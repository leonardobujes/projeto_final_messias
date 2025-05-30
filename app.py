from flask import Flask, render_template, url_for

app = Flask(__name__)

# Rota para a página inicial (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para selecao.html
@app.route('/selecao')
def selecao():
    return render_template('selecao.html')

# Rota para repeticao.html
@app.route('/repeticao')
def repeticao():
    return render_template('repeticao.html')

# Rota para vetores_matrizes.html
@app.route('/vetores_matrizes')
def vetores_matrizes():
    return render_template('vetores_matrizes.html')

# Rota para funcoes_procedimentos.html
@app.route('/funcoes_procedimentos')
def funcoes_procedimentos():
    return render_template('funcoes_procedimentos.html')

# Rota para excecoes.html
@app.route('/excecoes')
def excecoes():
    return render_template('excecoes.html')

# Rota para equipe.html
@app.route('/equipe')
def equipe():
    return render_template('equipe.html')

if __name__ == '__main__':
    # Executa a aplicação em modo de depuração
    # Ouça em todas as interfaces (0.0.0.0) para permitir acesso externo se necessário
    app.run(host='0.0.0.0', port=5000, debug=True)

