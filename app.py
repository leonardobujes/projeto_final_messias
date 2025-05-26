from flask import Flask, render_template, request, redirect, url_for, flash

# Inicializa a aplicação Flask
app = Flask(__name__)

# Configuração de uma chave secreta para usar flash messages (boas para feedback ao usuário)
# Em um ambiente de produção, use uma chave mais segura e, de preferência, configure via variáveis de ambiente.
app.secret_key = 'sua_chave_secreta_aqui' # Troque por uma chave forte e aleatória

# Dados de exemplo (simulando um pequeno "banco de dados" em memória)
artigos_blog = [
    {"id": 1, "titulo": "Primeiros Passos com Flask", "conteudo": "Flask é um microframework leve..."},
    {"id": 2, "titulo": "Templates com Jinja2", "conteudo": "Jinja2 é o motor de templates padrão do Flask..."},
    {"id": 3, "titulo": "Rotas e Views no Flask", "conteudo": "Rotas definem as URLs da sua aplicação..."}
]

# Rota para a página inicial
@app.route('/')
def index():
    """
    Rota para a página inicial.
    Renderiza o template index.html passando uma lista de artigos.
    """
    return render_template('index.html', artigos=artigos_blog, titulo_pagina="Página Inicial")

# Rota para a página "Sobre"
@app.route('/sobre')
def sobre():
    """
    Rota para a página "Sobre".
    Renderiza o template sobre.html.
    """
    return render_template('sobre.html', titulo_pagina="Sobre Nós")

# Rota para a página de "Contato", aceita GET (para mostrar o formulário) e POST (para enviar os dados)
@app.route('/contato', methods=['GET', 'POST'])
def contato():
    """
    Rota para a página de contato.
    Se o método for POST, processa os dados do formulário.
    Se for GET, exibe o formulário.
    """
    if request.method == 'POST':
        # Aqui você pegaria os dados do formulário
        nome = request.form.get('nome')
        email = request.form.get('email')
        assunto = request.form.get('assunto')
        mensagem = request.form.get('mensagem')

        # Validação simples (em uma aplicação real, seria mais robusta)
        if not nome or not email or not mensagem:
            flash('Por favor, preencha todos os campos obrigatórios (Nome, Email, Mensagem).', 'danger')
            return redirect(url_for('contato')) # Redireciona de volta para o formulário

        # Simulação do envio de e-mail ou salvamento no banco de dados
        print(f"Nova mensagem de contato recebida:")
        print(f"Nome: {nome}")
        print(f"Email: {email}")
        print(f"Assunto: {assunto}")
        print(f"Mensagem: {mensagem}")

        # Adiciona uma mensagem flash de sucesso
        flash('Sua mensagem foi enviada com sucesso!', 'success')

        # Redireciona para uma página de confirmação ou para a própria página de contato
        # return redirect(url_for('mensagem_enviada'))
        return redirect(url_for('contato')) # Redireciona para a mesma página para ver a flash message

    # Se o método for GET, apenas renderiza o template do formulário
    return render_template('contato.html', titulo_pagina="Contato")

# Rota de exemplo para uma página de confirmação (opcional)
@app.route('/mensagem-enviada')
def mensagem_enviada():
    """
    Rota para uma página de confirmação após o envio do formulário.
    """
    return render_template('mensagem_enviada.html', titulo_pagina="Mensagem Enviada")


# Rota para visualizar um artigo específico (exemplo de rota com parâmetro)
@app.route('/artigo/<int:artigo_id>')
def ver_artigo(artigo_id):
    """
    Rota para visualizar um artigo específico pelo seu ID.
    """
    artigo_encontrado = None
    for artigo in artigos_blog:
        if artigo['id'] == artigo_id:
            artigo_encontrado = artigo
            break

    if artigo_encontrado:
        return render_template('artigo.html', artigo=artigo_encontrado, titulo_pagina=artigo_encontrado['titulo'])
    else:
        flash(f'Artigo com ID {artigo_id} não encontrado.', 'warning')
        return redirect(url_for('index'))


# Verifica se o script está sendo executado diretamente para rodar o servidor de desenvolvimento
if __name__ == '__main__':
    # app.run() é para produção quando usado com um servidor WSGI como Gunicorn
    # Para desenvolvimento, use debug=True para auto-reload e debugger interativo
    app.run(debug=True, port=5001) # Você pode mudar a porta se a 5000 estiver em uso
