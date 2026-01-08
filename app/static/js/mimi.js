// mimi.js - Chat frontend para integração com Ollama API

document.addEventListener('DOMContentLoaded', function () {
    const chatForm = document.querySelector('.mimi-chat-form');
    const chatBox = document.querySelector('.mimi-chat-box');
    const input = chatForm.querySelector('input[type="text"]');
    const convList = document.querySelector('.mimi-conv-list');
    const btnNewConv = document.querySelector('.btn-new-conv');

    let currentConvId = null;
    let isNewConv = true;


    // Função para obter prefixo de URL (igual ao backend)
    function getPrefix() {
        // Tenta obter do template, fallback para vazio
        if (window.get_url_prefix) return window.get_url_prefix();
        if (window.STUDYHUB_PREFIX) return window.STUDYHUB_PREFIX;
        // Detecta por path
        if (window.location.pathname.startsWith('/studyhubai/')) return '/studyhubai';
        return '';
    }
    const prefix = getPrefix();

    // Carrega histórico de conversas na sidebar
    async function loadConversations() {
        convList.innerHTML = '<li style="color:#aaa;text-align:center;">Carregando...</li>';
        try {
            const res = await fetch(`${prefix}/mimi/api/conversations`);
            const data = await res.json();
            convList.innerHTML = '';
            if (data.length === 0) {
                convList.innerHTML = '<li style="color:#aaa;text-align:center;">Nenhuma conversa ainda.</li>';
            } else {
                data.forEach(conv => {
                    const li = document.createElement('li');
                    li.className = 'mimi-conv-item';
                    li.style = 'padding:0.5rem 0.7rem;cursor:pointer;border-radius:6px;margin-bottom:0.3rem;color:#fff;';
                    li.textContent = conv.question.slice(0, 32) + (conv.question.length > 32 ? '...' : '');
                    li.title = conv.question;
                    // Sempre use conv.conversation_id (que é igual ao id da primeira mensagem)
                    li.onclick = () => loadConversation(conv.conversation_id);
                    convList.appendChild(li);
                });
            }
        } catch (err) {
            convList.innerHTML = '<li style="color:#f66;text-align:center;">Erro ao carregar histórico.</li>';
        }
    }

    // Carrega uma conversa específica no chat
    async function loadConversation(convId) {
        chatBox.innerHTML = '<div style="color:#aaa;text-align:center;">Carregando conversa...</div>';
        try {
            const res = await fetch(`${prefix}/mimi/api/conversations/${convId}`);
            const convs = await res.json();
            chatBox.innerHTML = '';
            // Se vier um array, exibe todo o histórico; se for objeto, exibe só uma troca
            if (Array.isArray(convs)) {
                convs.forEach(msg => {
                    addMessage(msg.question, 'user');
                    addMessage(msg.answer, 'bot');
                });
                // currentConvId deve ser o conversation_id da thread (primeira mensagem)
                if (convs.length > 0) {
                    currentConvId = convs[0].conversation_id;
                }
            } else {
                addMessage(convs.question, 'user');
                addMessage(convs.answer, 'bot');
                currentConvId = convs.conversation_id;
            }
            isNewConv = false;
        } catch (err) {
            chatBox.innerHTML = '<div style="color:#f66;text-align:center;">Erro ao carregar conversa.</div>';
        }
    }


    // Nova conversa (se botão existir)
    if (btnNewConv) {
        btnNewConv.addEventListener('click', function () {
            chatBox.innerHTML = '';
            currentConvId = null;
            isNewConv = true;
        });
    }

    // Envio de mensagem
    chatForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const userMsg = input.value.trim();
        if (!userMsg) return;
        addMessage(userMsg, 'user');
        input.value = '';
        try {
            // Só envie conversation_id se for um número válido
            let body = { message: userMsg };
            if (typeof currentConvId === 'number' && !isNaN(currentConvId)) {
                body.conversation_id = currentConvId;
            }
            const res = await fetch(`${prefix}/mimi/api/ask`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            const data = await res.json();
            addMessage(data.response, 'bot');
            // Atualiza currentConvId se backend retornar conversation_id
            if (data.conversation_id) {
                currentConvId = data.conversation_id;
            }
            // Após enviar, recarrega histórico
            loadConversations();
        } catch (err) {
            addMessage('Erro ao conectar com a IA.', 'bot');
        }
    });

    function addMessage(text, who) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'mimi-message ' + (who === 'user' ? 'user' : '');
        if (who === 'bot') {
            // Formatação especial para resposta da Mimi
            msgDiv.innerHTML = `
                <div class="mimi-avatar"><img src="https://www.thecarv.com/studyhubai/static/img/mimi.png" /></div>
                <div class="mimi-message-content" style="background: linear-gradient(120deg, #7c3aed33 60%, #fff2 100%); border: 2px solid #7c3aed44; box-shadow: 0 2px 16px #7c3aed22; font-style: italic; color: #e6e6ff; font-family: 'Segoe UI', 'Roboto', sans-serif; letter-spacing: 0.01em;">${formatMimiText(text)}</div>
            `;
        } else {
            msgDiv.innerHTML = `
                <div class="mimi-avatar"><img src="https://www.thecarv.com/studyhubai/static/img/user.png" /></div>
                <div class="mimi-message-content">${text}</div>
            `;
        }
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Função para formatar texto da Mimi
    function formatMimiText(text) {
        // Remove menções ao nome, se houver
        let t = text.replace(/\bMimi\b/gi, "");
        // Opcional: outras formatações, como aspas, emojis, etc.
        // Exemplo: adicionar aspas se for uma resposta longa
        if (t.length > 80) {
            t = '“' + t.trim() + '”';
        }
        return t.trim();
    }
    // Inicialização
    loadConversations();
});
