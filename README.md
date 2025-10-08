# ESTG-ESII-StudyHub Ai
Projeto Final de Engenharia de Software II

StudyHub AI

O StudyHub AI é uma plataforma web desenvolvida para a disciplina de Engenharia de Software II. O objetivo é ajudar estudantes a criar e participar em grupos de estudo, partilhar materiais e tirar dúvidas de forma mais eficiente com o auxílio de um assistente de IA.

---

Equipa do Projeto

* [Thaissa Rodrigues  - 2022128743] - [Link para o perfil do GitHub]
* [Lara Silva - 2024127613 ] - [Link para o perfil do GitHub]
* [Pedro Carvalho - 2024114495] - [Link para o perfil do GitHub]
* [Sarah Ellen - 2024120265] - [Link para o perfil do GitHub]

---

Tecnologias Utilizadas

* **Backend:** Python com o framework Django
* **Frontend:** HTML, CSS, JavaScript
* **Base de Dados:** SQLite (para desenvolvimento)
* **LLM:** Ollama (executado localmente)

---

Como Executar o Projeto Localmente

1.  **Clonar o repositório:**
    ```bash
    git clone [https://repositorium.sdum.uminho.pt/handle/1822/414](https://repositorium.sdum.uminho.pt/handle/1822/414)
    cd ESTG-ESII-StudyHub-AI
    ```

2.  **Criar e ativar um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instalar as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplicar as migrações da base de dados:**
    ```bash
    python manage.py migrate
    ```

5.  **Executar o servidor de desenvolvimento:**
    ```bash
    python manage.py runserver
    ```
