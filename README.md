# StudyHub AI 🎓

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)

> **Plataforma web inteligente para estudantes criarem grupos de estudo colaborativos**

Uma aplicação desenvolvida para a disciplina de **Engenharia de Software II** que revoluciona a forma como estudantes se conectam, colaboram e aprendem juntos, com o poder da Inteligência Artificial.


## 📋 Sobre o Projeto

O **StudyHub AI** é uma plataforma web inovadora que visa facilitar a criação e gestão de grupos de estudo entre estudantes. Com funcionalidades modernas e um assistente de IA integrado, a plataforma oferece um ambiente completo para:

- 👥 **Criação de grupos de estudo** personalizados por matéria/tema
- 📚 **Partilha de materiais** educativos entre membros
- 🤖 **Assistente de IA** para esclarecimento de dúvidas
- 💬 **Sistema de comunicação** em tempo real
- 📊 **Acompanhamento do progresso** de estudos

## ✨ Funcionalidades

### 🔐 Autenticação e Perfis
- Registo e login de utilizadores
- Perfis personalizados de estudantes
- Gestão de preferências de estudo

### 👥 Gestão de Grupos
- Criação de grupos por disciplina/matéria
- Sistema de convites e aprovações
- Definição de objetivos e metas do grupo
- Calendário de sessões de estudo

### 📁 Partilha de Recursos
- Upload e organização de materiais de estudo
- Categorização por tipo de conteúdo
- Sistema de comentários e avaliações
- Controlo de versões de documentos

### 🤖 Assistente IA Integrado
- Esclarecimento de dúvidas em tempo real
- Sugestões de estudo personalizadas
- Geração de resumos automáticos
- Recomendações de recursos complementares

### 📊 Analytics e Progresso
- Métricas de participação individual
- Estatísticas de performance do grupo
- Relatórios de progresso de aprendizagem

## 🏗️ Arquitetura do Sistema

```
ESTG-ES2-Final-project/
├── 📁 app/                    # Aplicação principal
│   ├── 📁 models/            # Modelos de dados (SQLAlchemy)
│   ├── 📁 modules/           # Módulos funcionais da aplicação
│   ├── 📁 static/            # Ficheiros estáticos (CSS, JS, imagens)
│   ├── 📁 templates/         # Templates HTML (Jinja2)
│   ├── 📁 utils/             # Utilitários e funções auxiliares
│   └── 📄 __init__.py        # Inicialização da aplicação Flask
├── 📁 instance/              # Configurações específicas da instância
├── 📁 test/                  # Testes unitários e de integração
├── 📄 run.py                 # Ponto de entrada da aplicação
└── 📄 README.md              # Documentação do projeto
```

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+** - Linguagem principal
- **Flask** - Framework web
- **SQLAlchemy** - ORM para base de dados
- **Flask-Login** - Gestão de autenticação
- **Flask-WTF** - Formulários e validação

### Frontend
- **HTML5/CSS3** - Estrutura e estilização
- **JavaScript** - Interatividade
- **Bootstrap** - Framework CSS responsivo
- **Jinja2** - Motor de templates

### Base de Dados
- **SQLite** (desenvolvimento)
- **PostgreSQL** (produção)

### IA e Machine Learning
- **Ollama** - Assistente inteligente
- **Natural Language Processing** - Processamento de texto

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- pip (gestor de pacotes Python)
- Git

### 1. Clonar o Repositório
```bash
git clone https://github.com/Pedrocarv007/ESTG-ES2-Final-project.git
cd ESTG-ES2-Final-project
```

### 2. Criar Ambiente Virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/macOS
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
Criar ficheiro `.env` na raiz do projeto:
```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///studyhub.db
OPENAI_API_KEY=your-openai-api-key
```

### 5. Inicializar Base de Dados
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Executar a Aplicação
```bash
python run.py
```

A aplicação estará disponível em `http://localhost:5000`

## 🧪 Testes

Para executar os testes:
```bash
python -m pytest test/ -v
```

Para cobertura de código:
```bash
python -m pytest test/ --cov=app --cov-report=html
```

## 📚 Documentação da API

A documentação completa da API está disponível em:
- **Desenvolvimento**: `http://localhost:5000/api/docs`
- **Swagger UI**: Documentação interativa da API

### Principais Endpoints
- `POST /api/auth/login` - Autenticação de utilizador
- `GET /api/groups` - Listar grupos de estudo
- `POST /api/groups` - Criar novo grupo
- `POST /api/groups/{id}/join` - Juntar-se a um grupo
- `GET /api/materials` - Listar materiais de estudo
- `POST /api/ai/ask` - Interagir com assistente IA

## 🤝 Contribuição

### Como Contribuir
1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Padrões de Código
- Seguir PEP 8 para Python
- Documentar funções e classes
- Escrever testes para novas funcionalidades
- Manter cobertura de testes acima de 80%

## 📈 Roadmap

### Versão 1.0 (Atual)
- [x] Sistema de autenticação
- [x] Criação de grupos básicos
- [x] Upload de ficheiros
- [x] Chat básico

### Versão 1.1 (Próxima)
- [ ] Assistente IA avançado
- [ ] Notificações em tempo real
- [ ] Sistema de gamificação
- [ ] App mobile (React Native)

### Versão 2.0 (Futuro)
- [ ] Integração com LMS
- [ ] Análise de sentimentos
- [ ] Recomendações personalizadas
- [ ] API pública

## 👥 Equipa de Desenvolvimento

| Nome | Papel | GitHub |
|------|-------|--------|
| Pedro | Full-Stack Developer | [@Pedrocarv007](https://github.com/Pedrocarv007) |
| Lara  | Full-Stack Developer | [@Larajen9](https://github.com/Larajen9)|
| Thaissa | Full-Stack Developer | [@Devthaissa1](https://github.com/Devthaissa1)|
| Sarah | Full-Stack Developer | [@Saretesson](https://github.com/Saretesson)|



<div align="center">
  <strong>Desenvolvido com ❤️ para a comunidade estudantil</strong>
  <br>
  <em>StudyHub AI - Transformando a educação através da colaboração inteligente</em>
</div>