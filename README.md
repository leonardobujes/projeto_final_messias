# Projeto Final: Fundamentos de Programação em Python com Flask

Este projeto consiste numa aplicação web interativa desenvolvida com o framework Flask. O objetivo é criar um site informativo sobre os fundamentos da programação em Python, incluindo uma funcionalidade de perguntas e respostas integrada com a API do Gemini (simulada neste exemplo) e um dicionário interativo de termos de programação com persistência em arquivo de texto (CSV).

## Estrutura do Site e Conteúdo de Cada Seção

O site está organizado da seguinte forma:

* **`/` (Início):** Página inicial de boas-vindas.
* **`/selecao` (Estruturas de Seleção):** Explica o conceito de `if`, `elif`, `else`, suas aplicações e exemplos de código.
* **`/repeticao` (Estruturas de Repetição):** Detalha os laços `for` e `while`, com aplicações e exemplos.
* **`/vetores_matrizes` (Vetores e Matrizes):** Aborda listas (como vetores) e listas de listas (como matrizes) em Python, com exemplos.
* **`/funcoes_procedimentos` (Funções e Procedimentos):** Discute a definição e uso de funções (com e sem retorno) em Python.
* **`/excecoes` (Tratamento de Exceções):** Explica os blocos `try`, `except`, `else`, `finally` para lidar com erros.
* **`/tirar-duvidas` (Tirar Dúvidas):** Uma seção interativa onde os utilizadores podem submeter perguntas sobre programação (Python, Flask, etc.) e receber respostas geradas por uma IA (simulação da API do Gemini).
* **`/glossario` (Glossário):** Apresenta uma lista de termos de programação com as suas definições. Permite:
    * Visualizar todos os termos.
    * Adicionar novos termos e definições.
    * Alterar termos e definições existentes.
    * Eliminar termos.
    Os dados do glossário são armazenados no arquivo `bd_glossario.csv`.
* **`/equipe` (Equipe):** Apresenta os membros da equipe que desenvolveram o projeto, com links para os seus perfis profissionais (ex: LinkedIn, GitHub).

## Tecnologias Utilizadas

* **Linguagem de Programação:** Python 3.x
* **Framework Web:** Flask
* **Frontend:** HTML5, CSS3, JavaScript (básico para menu responsivo)
* **Armazenamento de Dados (Glossário):** Arquivo CSV (`bd_glossario.csv`)
* **API de IA (para "Tirar Dúvidas"):** Google Gemini API (a integração real requer uma chave de API e a biblioteca `google-generativeai`). No código fornecido, esta funcionalidade é simulada.

## Integração com a API do Gemini (Simulada)

A seção "Tirar Dúvidas" (`/tirar-duvidas`) foi projetada para interagir com a API do Gemini.

1.  **Interface do Utilizador:**
    * Um formulário HTML permite que o utilizador submeta uma pergunta.
2.  **Backend (Flask - `app.py`):**
    * A rota `/tirar-duvidas` recebe a pergunta via método POST.
    * **Ponto de Integração (Simulado):** Dentro da função `tirar_duvidas()` em `app.py`, há um bloco de código comentado que indica onde a chamada real à API do Gemini ocorreria.
        ```python
        # try:
        #     # --- INÍCIO DA CHAMADA REAL À API DO GEMINI ---
        #     # GOOGLE_API_KEY = 'SUA_CHAVE_API_AQUI' # Carregar de forma segura
        #     # genai.configure(api_key=GOOGLE_API_KEY)
        #     # model = genai.GenerativeModel('gemini-pro')
        #     # response = model.generate_content(pergunta_usuario)
        #     # resposta_gemini = response.text
        #     # --- FIM DA CHAMADA REAL À API DO GEMINI ---
        #
        #     # Simulação atual:
        #     if "python" in pergunta_usuario.lower():
        #         resposta_gemini = f"Resposta simulada para '{pergunta_usuario}': Python é..."
        #     # ...
        # except Exception as e:
        #     resposta_gemini = f"Ocorreu um erro ao processar sua pergunta: {e}"
        ```
    * Para a integração real:
        * Descomente as linhas relevantes.
        * Substitua `'SUA_CHAVE_API_AQUI'` pela sua chave de API válida do Google Gemini.
        * Certifique-se de que a biblioteca `google-generativeai` está instalada (`pip install google-generativeai`).
3.  **Exibição da Resposta:** A resposta (real ou simulada) é passada de volta para o template `tirar_duvidas.html` e exibida ao utilizador.

## Como Executar a Aplicação Flask Localmente

1.  **Pré-requisitos:**
    * Python 3.x instalado.
    * `pip` (gerenciador de pacotes do Python) instalado.

2.  **Clonar o Repositório (se aplicável):**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DA_PASTA_DO_PROJETO>
    ```

3.  **Criar e Ativar um Ambiente Virtual (Recomendado):**
    ```bash
    python -m venv venv
    # No Windows:
    venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```

4.  **Instalar as Dependências:**
    Crie um arquivo `requirements.txt` com o seguinte conteúdo:
    ```txt
    Flask
    # google-generativeai # Adicione se for implementar a API do Gemini
    ```
    Depois, instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
    Se não usar `requirements.txt`, instale o Flask diretamente:
    ```bash
    pip install Flask
    # pip install google-generativeai # Se for usar Gemini
    ```

5.  **Estrutura de Pastas Esperada:**
    Certifique-se de que a estrutura do seu projeto está correta:
    ```
    seu_projeto/
    ├── app.py
    ├── bd_glossario.csv  (será criado ou pode ser criado manualmente)
    ├── README.md
    ├── requirements.txt (opcional, mas recomendado)
    ├── static/
    │   └── css/
    │       └── style.css
    └── templates/
        ├── index.html
        ├── selecao.html
        ├── repeticao.html
        ├── vetores_matrizes.html
        ├── funcoes_procedimentos.html
        ├── excecoes.html
        ├── tirar_duvidas.html
        ├── glossario.html
        ├── alterar_termo.html
        └── equipe.html
    ```

6.  **Executar a Aplicação:**
    No terminal, navegue até a pasta raiz do projeto (onde `app.py` está localizado) e execute:
    ```bash
    python app.py
    ```
    Ou, usando o comando Flask (se configurado corretamente):
    ```bash
    flask run
    ```

7.  **Aceder à Aplicação:**
    Abra o seu navegador e vá para `http://127.0.0.1:5000/` ou `http://localhost:5000/`.

## Descrição das Principais Partes do Código Python (`app.py`)

* **Inicialização do Flask:**
    ```python
    from flask import Flask, render_template, request, redirect, url_for, flash
    import csv
    import os
    app = Flask(__name__)
    app.secret_key = 'supersecretkey' # Para flash messages
    CSV_FILE = 'bd_glossario.csv'
    ```
* **Funções do Glossário:**
    * `carregar_glossario()`: Lê os dados do `bd_glossario.csv` e retorna uma lista de dicionários. Cada dicionário representa um termo e inclui um `id` (índice) para facilitar a edição/eliminação.
    * `salvar_glossario(glossario_data)`: Recebe uma lista de dicionários e reescreve o arquivo `bd_glossario.csv` com os dados atualizados.
* **Rotas de Conteúdo Estático:**
    * Rotas como `@app.route('/')`, `@app.route('/selecao')`, etc., simplesmente renderizam os templates HTML correspondentes, passando o `page_name` para realçar o item de menu ativo.
* **Rotas do Glossário (CRUD):**
    * `@app.route('/glossario')` (GET): Exibe a página do glossário, carregando os termos.
    * `@app.route('/glossario/adicionar', methods=['POST'])`: Recebe dados do formulário de adição, valida, adiciona o novo termo à lista e salva no CSV. Usa `flash` para mensagens de feedback.
    * `@app.route('/glossario/alterar/<int:termo_id>', methods=['GET', 'POST'])`:
        * GET: Exibe o formulário `alterar_termo.html` pré-preenchido com os dados do termo selecionado pelo `termo_id`.
        * POST: Recebe os dados alterados, atualiza o termo na lista e salva no CSV.
    * `@app.route('/glossario/eliminar/<int:termo_id>', methods=['POST'])`: Remove o termo correspondente ao `termo_id` da lista e salva as alterações no CSV.
* **Rota "Tirar Dúvidas":**
    * `@app.route('/tirar-duvidas', methods=['GET', 'POST'])`:
        * GET: Exibe o formulário para o utilizador inserir a pergunta.
        * POST: Recebe a pergunta, simula uma chamada à API do Gemini e exibe a resposta simulada. O local para a integração real com a API do Gemini está indicado nos comentários.
* **Execução da Aplicação:**
    ```python
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000, debug=True)
    ```
    Inicia o servidor de desenvolvimento do Flask.