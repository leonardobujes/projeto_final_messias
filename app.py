from flask import Flask, render_template, url_for
import csv # Importa o módulo csv para ler o arquivo

app = Flask(__name__)

# Função auxiliar para ler o glossário do CSV
def carregar_glossario():
    glossario = []
    try:
        with open('bd_glossario.csv', mode='r', encoding='utf-8') as file:
            # Usar ; como delimitador
            csv_reader = csv.reader(file, delimiter=';') 
            for row in csv_reader:
                if len(row) == 2: # Espera duas colunas: Termo;Definicao
                    glossario.append({'termo': row[0], 'definicao': row[1]})
                elif len(row) > 0 and not row[0].strip().startswith('#') and any(field.strip() for field in row):
                    # Log ou tratamento para linhas com formato inesperado que não são comentários e não estão vazias
                    print(f"Aviso: Linha ignorada no CSV por formato inesperado: {row}")
    except FileNotFoundError:
        print("Erro: Arquivo bd_glossario.csv não encontrado.")
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
    return glossario

# Rota para a página inicial (index.html)
@app.route('/')
def index():
    return render_template('index.html', page_name='index')

# Rota para selecao.html
@app.route('/selecao')
def selecao():
    return render_template('selecao.html', page_name='selecao')

# Rota para repeticao.html
@app.route('/repeticao')
def repeticao():
    return render_template('repeticao.html', page_name='repeticao')

# Rota para vetores_matrizes.html
@app.route('/vetores_matrizes')
def vetores_matrizes():
    return render_template('vetores_matrizes.html', page_name='vetores_matrizes')

# Rota para funcoes_procedimentos.html
@app.route('/funcoes_procedimentos')
def funcoes_procedimentos():
    return render_template('funcoes_procedimentos.html', page_name='funcoes_procedimentos')

# Rota para excecoes.html
@app.route('/excecoes')
def excecoes():
    return render_template('excecoes.html', page_name='excecoes')

# Rota para equipe.html
@app.route('/equipe')
def equipe():
    return render_template('equipe.html', page_name='equipe')

# Nova rota para o glossário
@app.route('/glossario')
def glossario_page():
    termos_glossario = carregar_glossario()
    return render_template('glossario.html', page_name='glossario', termos=termos_glossario)


if __name__ == '__main__':
    # Executa a aplicação em modo de depuração
    # Ouça em todas as interfaces (0.0.0.0) para permitir acesso externo se necessário
    app.run(host='0.0.0.0', port=5000, debug=True)
