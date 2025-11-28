"""
Main application routes
"""
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from app.main import bp
from math import ceil

# --- DADOS FALSOS PARA TESTAR O FRONTEND ---
GROUPS_DATA = [
    # Página 1
    {'id': 1, 'name': 'Graphic Design', 'type': 'public', 'members': 293, 'active': '7 dias atrás', 'img': 'gato.jpg', 'desc': 'Aprende os fundamentos do design, teoria da cor e tipografia.'},
    {'id': 2, 'name': 'Art Group', 'type': 'private', 'members': 120, 'active': '2 dias atrás', 'img': 'gatinho.jpg', 'desc': 'Grupo exclusivo para estudantes de Belas Artes.'},
    {'id': 3, 'name': 'UX/UI Design', 'type': 'public', 'members': 500, 'active': '1 hora atrás', 'img': 'pombo.jpg', 'desc': 'Focado em experiência do utilizador e interfaces web.'},
    {'id': 4, 'name': 'Typography', 'type': 'public', 'members': 89, 'active': '5 min atrás', 'img': '', 'placeholder': 'Aa', 'desc': 'Tudo sobre fontes e letras.'},
    {'id': 5, 'name': 'Python Devs', 'type': 'public', 'members': 1200, 'active': 'Hoje', 'img': '', 'placeholder': '🐍', 'desc': 'Programação em Python, Django e Flask.'},
    {'id': 6, 'name': 'Calculus II', 'type': 'private', 'members': 45, 'active': '3 dias atrás', 'img': '', 'placeholder': '∫', 'desc': 'Preparação para o exame de Cálculo.'},
    
    # Página 2 
    {'id': 7, 'name': 'Biology 101', 'type': 'public', 'members': 340, 'active': 'Ontem', 'img': '', 'placeholder': '🧬', 'desc': 'Estudo de anatomia e biologia celular.'},
    {'id': 8, 'name': 'Marketing Digital', 'type': 'public', 'members': 800, 'active': 'Agora', 'img': '', 'placeholder': '📈', 'desc': 'Estratégias de SEO, Social Media e Ads.'},
    {'id': 9, 'name': 'Machine Learning', 'type': 'private', 'members': 60, 'active': '1 semana atrás', 'img': '', 'placeholder': '🤖', 'desc': 'Grupo de estudo avançado sobre IA e Redes Neurais.'},
    {'id': 10, 'name': 'English Conversation', 'type': 'public', 'members': 150, 'active': '10 min atrás', 'img': '', 'placeholder': '💬', 'desc': 'Pratica o teu inglês com outros estudantes.'},
    {'id': 11, 'name': 'Photography', 'type': 'public', 'members': 210, 'active': '4 dias atrás', 'img': '', 'placeholder': '📷', 'desc': 'Dicas de iluminação, composição e edição.'},
    {'id': 12, 'name': 'Physics Lab', 'type': 'private', 'members': 30, 'active': 'Hoje', 'img': '', 'placeholder': '⚛️', 'desc': 'Relatórios de laboratório de Física I e II.'},

    # Página 3 
    {'id': 13, 'name': 'Web3 & Blockchain', 'type': 'public', 'members': 400, 'active': '2 horas atrás', 'img': '', 'placeholder': '⛓️', 'desc': 'O futuro da internet, crypto e smart contracts.'},
    {'id': 14, 'name': 'Game Dev Unity', 'type': 'public', 'members': 650, 'active': 'Hoje', 'img': '', 'placeholder': '🎮', 'desc': 'Criação de jogos 2D e 3D com Unity e C#.'},
    {'id': 15, 'name': 'History of Art', 'type': 'public', 'members': 90, 'active': '1 mês atrás', 'img': '', 'placeholder': '🎨', 'desc': 'Do Renascimento à Arte Moderna.'},
    {'id': 16, 'name': 'Cybersecurity', 'type': 'private', 'members': 55, 'active': 'Ontem', 'img': '', 'placeholder': '🔒', 'desc': 'Ethical Hacking e segurança de redes.'},
    {'id': 17, 'name': 'Music Theory', 'type': 'public', 'members': 110, 'active': '3 dias atrás', 'img': '', 'placeholder': '🎵', 'desc': 'Harmonia, composição e leitura de partituras.'},
    {'id': 18, 'name': 'Architecture', 'type': 'public', 'members': 320, 'active': '5 horas atrás', 'img': '', 'placeholder': '🏛️', 'desc': 'Projectos, maquetes e história da arquitetura.'}
]

#ROTAS PÚBLICAS

@bp.route('/')
@bp.route('/home')
def index():
    """Home page route."""
    return render_template('index.html', active_page='index')

@bp.route('/about')
def about():
    """About page route."""
    return render_template('about.html', active_page='about')

@bp.route('/contacts')
def contacts():
    """Contact page route."""
    return render_template('contacts.html', active_page='contacts')

@bp.route('/groups')
def groups():
    # 1. Parâmetros da URL
    filter_type = request.args.get('filter', 'all')
    search_query = request.args.get('q', '').lower()
    page = request.args.get('page', 1, type=int) # Página atual (padrão 1)
    per_page = 6 # Quantos grupos por página?
    
    # 2. Filtragem
    filtered_groups = GROUPS_DATA
    
    if filter_type == 'public':
        filtered_groups = [g for g in GROUPS_DATA if g['type'] == 'public']
    elif filter_type == 'private':
        filtered_groups = [g for g in GROUPS_DATA if g['type'] == 'private']
    
    if search_query:
        filtered_groups = [g for g in filtered_groups if search_query in g['name'].lower()]

    # 3. Lógica de Paginação (Slice da lista)
    total_groups = len(filtered_groups)
    total_pages = ceil(total_groups / per_page)
    
    start = (page - 1) * per_page
    end = start + per_page
    
    # Pega apenas os grupos da página atual
    current_page_groups = filtered_groups[start:end]

    # Contagens para as abas
    counts = {
        'all': len(GROUPS_DATA),
        'public': len([g for g in GROUPS_DATA if g['type'] == 'public']),
        'private': len([g for g in GROUPS_DATA if g['type'] == 'private']),
        'my': 10
    }

    return render_template('groups.html', 
                           groups=current_page_groups, # Envia apenas os 6 da página
                           active_page='groups',
                           current_filter=filter_type,
                           counts=counts,
                           current_page=page,     # Para saber qual botão pintar
                           total_pages=total_pages # Para saber quantos botões criar
                           )

@bp.route('/groups/<int:group_id>')
def group_detail(group_id):
    # Procura o grupo na lista falsa pelo ID
    group = next((g for g in GROUPS_DATA if g['id'] == group_id), None)
    if not group:
        return "Grupo não encontrado (404)", 404
    return render_template('group_detail.html', group=group)

#ROTAS PRIVADAS

@bp.route('/dashboard')
@login_required # Isso serve para proteger a rota.
def dashboard():
    """Dashboard route."""
    return render_template('dashboard.html', active_page='dashboard')


#ROTAS A IMPLEMENTAR

@bp.route('/materials')
@login_required
def materials():
    """Materials route."""
    return render_template('wip.html', active_page='materials') 

@bp.route('/mimi_ai')
@login_required
def mimi_ai():
    """Mimi AI route."""
    return render_template('wip.html', active_page='mimi_ai') 

@bp.route('/progress')
@login_required
def progress():
    """Progress route."""
    return render_template('wip.html', active_page='progress') 

@bp.route('/calendar')
@login_required
def calendar():
    """Calendar route."""
    return render_template('wip.html', active_page='calendar') 

@bp.route('/settings')
@login_required
def settings():
    return render_template('wip.html', active_page='settings') 