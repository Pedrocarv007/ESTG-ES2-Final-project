
from flask import Blueprint, redirect, request, jsonify, url_for, render_template
from flask_login import current_user, login_required
import requests
from app.extensions import csrf
from app.models import AIConversation
from app.config.database import db

# API AI Assistant endpoints
mimi = Blueprint('mimi', __name__)

# Endpoint para buscar uma conversa específica por id
@mimi.route('/api/conversations/<int:conv_id>', methods=['GET'])
@login_required
def get_conversation(conv_id):
    # Busca todas as mensagens da thread (conversation_id = conv_id ou id = conv_id)
    # Primeiro, encontra o conversation_id correto
    conv = AIConversation.query.filter_by(id=conv_id, user_id=current_user.id).first()
    if conv is None:
        # Talvez conv_id seja um conversation_id, não id
        convs = AIConversation.query.filter_by(conversation_id=conv_id, user_id=current_user.id).order_by(AIConversation.created_at.asc()).all()
        if not convs:
            return jsonify({'error': 'Conversa não encontrada.'}), 404
        return jsonify([c.to_dict() for c in convs])
    # Se conversation_id está setado, busca todas as mensagens desse thread
    if conv.conversation_id:
        convs = AIConversation.query.filter_by(conversation_id=conv.conversation_id, user_id=current_user.id).order_by(AIConversation.created_at.asc()).all()
        return jsonify([c.to_dict() for c in convs])
    else:
        # Mensagem isolada (primeira da thread)
        return jsonify([conv.to_dict()])

# Endpoint para listar histórico de conversas do usuário logado
@mimi.route('/api/conversations', methods=['GET'])
@login_required
def list_conversations():
    # Lista apenas a primeira mensagem de cada thread (id == conversation_id ou conversation_id IS NULL)
    from sqlalchemy import or_, and_
    convs = AIConversation.query.filter_by(user_id=current_user.id).filter(
        or_(AIConversation.conversation_id == None, AIConversation.id == AIConversation.conversation_id)
    ).order_by(AIConversation.created_at.desc()).all()
    return jsonify([c.to_dict() for c in convs])

@mimi.route('/', methods=['GET'])
def hello():
    from flask_login import login_required
    from flask_login import current_user
    from flask import render_template
    return render_template('mimi_dashboard.html', active_page='mimi')


# Endpoint para receber perguntas do chat e conectar ao Ollama
@mimi.route('/api/ask', methods=['POST'])
@csrf.exempt
def ask_ollama():
    data = request.get_json()
    user_message = data.get('message', '')
    conversation_id = data.get('conversation_id')
    # Garante que conversation_id é inteiro válido ou None
    try:
        if conversation_id is not None and conversation_id != '' and conversation_id != 'null':
            conversation_id = int(conversation_id)
        else:
            conversation_id = None
    except Exception:
        conversation_id = None
    if not user_message:
        return jsonify({'response': 'Mensagem vazia.'}), 400

    try:
        ollama_url = 'http://localhost:11434/api/generate'
        payload = {
            'model': 'gpt-oss:120b-cloud',  # ou outro modelo disponível no Ollama
            'prompt': f'Você é uma assistente chamada Mimi. {user_message}',
            'stream': False
        }
        ollama_response = requests.post(ollama_url, json=payload, timeout=30)
        ollama_response.raise_for_status()
        import re
        result = ollama_response.json()
        answer = result.get('response', 'Sem resposta da IA.')
        # Markdown para HTML: negrito, itálico, tabelas
        answer = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', answer)
        answer = re.sub(r'\*(.*?)\*', r'<i>\1</i>', answer)

        # Tabelas Markdown para HTML
        def md_table_to_html(md):
            lines = [l.strip() for l in md.strip().split('\n') if l.strip()]
            if len(lines) < 2 or '|' not in lines[0]:
                return md
            # Detecta cabeçalho e separador
            header = lines[0].strip('|').split('|')
            sep = lines[1].strip('|').split('|')
            if not all('-' in s for s in sep):
                return md
            rows = [l.strip('|').split('|') for l in lines[2:]]
            html = '<table class="mimi-table"><thead><tr>'
            for h in header:
                html += f'<th>{h.strip()}</th>'
            html += '</tr></thead><tbody>'
            for r in rows:
                html += '<tr>' + ''.join(f'<td>{c.strip()}</td>' for c in r) + '</tr>'
            html += '</tbody></table>'
            return html

        # Substitui todas tabelas Markdown por HTML
        def replace_tables(text):
            # Regex para blocos de tabela Markdown
            table_re = re.compile(r'(?:^|\n)(\|.+\|\n\|[\- ]+\|(?:\n\|.*\|)+)', re.MULTILINE)
            return table_re.sub(lambda m: '\n' + md_table_to_html(m.group(1)), text)

        answer = replace_tables(answer)
    except Exception as e:
        answer = f'Erro ao conectar com Ollama: {str(e)}'

    # Salvar conversa no banco, se usuário autenticado
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        # Se não há conversation_id válido, cria nova thread (id será setado após commit)
        if not conversation_id:
            conv = AIConversation(user_id=current_user.id, question=user_message, answer=answer)
            db.session.add(conv)
            db.session.commit()
            # Atualiza conversation_id para o próprio id
            conv.conversation_id = conv.id
            db.session.commit()
        else:
            conv = AIConversation(user_id=current_user.id, question=user_message, answer=answer, conversation_id=conversation_id)
            db.session.add(conv)
            db.session.commit()

        return jsonify({'response': answer, 'conversation_id': conv.conversation_id})

    return jsonify({'response': answer})