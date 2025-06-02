from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os


GEMINI_AVAILABLE = False
gemini_model = None


try:
    import google.generativeai as genai
    GOOGLE_API_KEY = os.environ.get('GEMINI_API_KEY') 
    if not GOOGLE_API_KEY:
        GOOGLE_API_KEY = 'AIzaSyBSiM1b-XHivW5_dWep0mokQnC3M-T0nmQ'
        print("AVISO: Chave API do Gemini está no código. Considere usar variáveis de ambiente \\\para maior segurança.")

    if GOOGLE_API_KEY:
        genai.configure(api_key=GOOGLE_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')
        GEMINI_AVAILABLE = True
        print("INFO: Módulo Google Generative AI carregado e configurado com o modelo 'gemini-1.5-flash-latest'.")
    else:
        print("AVISO: Chave API do Gemini não encontrada. A funcionalidade 'Tirar Dúvidas' usará apenas simulação.")
        GEMINI_AVAILABLE = False

except ImportError:
    print("AVISO: Módulo google.generativeai não encontrado. A funcionalidade 'Tirar Dúvidas' usará apenas simulação.")
except Exception as e:
    print(f"ERRO: Ocorreu um erro ao configurar a API do Gemini: {e}. A funcionalidade 'Tirar Dúvidas' usará apenas simulação.")


app = Flask(__name__)
app.secret_key = 'supersecretkey_dev'  

# Caminho para o arquivo CSV do glossário
CSV_FILE = 'bd_glossario.csv'

# Função para LER o glossário do arquivo CSV
def carregar_glossario():
    glossario = []
    if not os.path.exists(CSV_FILE):
        return glossario
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8', newline='') as file:
            csv_reader = csv.reader(file, delimiter=';')
            for i, row in enumerate(csv_reader): 
                if len(row) == 2:
                    glossario.append({'id': i, 'termo': row[0].strip(), 'definicao': row[1].strip()})
                elif len(row) > 0 and not row[0].strip().startswith('#') and any(field.strip() for field in row):
                    print(f"Aviso: Linha {i+1} ignorada no CSV por formato inesperado: {row}")
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
    return glossario

# Função para SALVAR (reescrever) o glossário no arquivo CSV
def salvar_glossario(glossario_data):
    try:
        with open(CSV_FILE, mode='w', encoding='utf-8', newline='') as file:
            csv_writer = csv.writer(file, delimiter=';')
            for item in glossario_data:
                csv_writer.writerow([item['termo'], item['definicao']])
        return True 
    except Exception as e:
        print(f"Erro ao salvar o arquivo CSV: {e}")
        return False

# --- ROTAS PRINCIPAIS ---
@app.route('/')
def index():
    return render_template('index.html', page_name='index')

@app.route('/selecao')
def selecao():
    return render_template('selecao.html', page_name='selecao')

@app.route('/repeticao')
def repeticao():
    return render_template('repeticao.html', page_name='repeticao')

@app.route('/vetores_matrizes')
def vetores_matrizes():
    return render_template('vetores_matrizes.html', page_name='vetores_matrizes')

@app.route('/funcoes_procedimentos')
def funcoes_procedimentos():
    return render_template('funcoes_procedimentos.html', page_name='funcoes_procedimentos')

@app.route('/excecoes')
def excecoes():
    return render_template('excecoes.html', page_name='excecoes')

@app.route('/equipe')
def equipe():
    return render_template('equipe.html', page_name='equipe')

# --- ROTAS PARA OPERAÇÕES CRUD NO GLOSSÁRIO ---
@app.route('/glossario')
def glossario_page():
    termos_glossario = carregar_glossario() 
    return render_template('glossario.html', page_name='glossario', termos=termos_glossario)

@app.route('/glossario/adicionar', methods=['POST'])
def adicionar_termo():
    if request.method == 'POST':
        termo = request.form.get('termo')
        definicao = request.form.get('definicao')

        if not termo or not definicao:
            flash('Termo e definição são obrigatórios!', 'error')
        else:
            termos_glossario = carregar_glossario()
            if any(item['termo'].lower() == termo.lower() for item in termos_glossario):
                flash(f'O termo "{termo}" já existe no glossário.', 'warning')
            else:
                termos_glossario.append({'termo': termo.strip(), 'definicao': definicao.strip()})
                if salvar_glossario(termos_glossario): 
                    flash('Termo adicionado com sucesso!', 'success')
                else:
                    flash('Erro ao salvar o termo.', 'error')
    return redirect(url_for('glossario_page'))

@app.route('/glossario/alterar/<int:termo_id>', methods=['GET', 'POST'])
def alterar_termo(termo_id):
    termos_glossario = carregar_glossario() 
    termo_para_alterar = None
    
    if 0 <= termo_id < len(termos_glossario):
        termo_para_alterar = termos_glossario[termo_id]
    
    if termo_para_alterar is None:
        flash('Termo não encontrado.', 'error')
        return redirect(url_for('glossario_page'))

    if request.method == 'POST':
        novo_termo_str = request.form.get('termo')
        nova_definicao = request.form.get('definicao')

        if not novo_termo_str or not nova_definicao:
            flash('Termo e definição são obrigatórios!', 'error')
        else:
            # Verifica se o novo termo já existe (exceto se for o próprio termo sendo editado)
            if any(item['termo'].lower() == novo_termo_str.lower() and i != termo_id for i, item in enumerate(termos_glossario)):
                flash(f'O termo "{novo_termo_str}" já existe no glossário.', 'warning')
            else:
                termos_glossario[termo_id]['termo'] = novo_termo_str.strip()
                termos_glossario[termo_id]['definicao'] = nova_definicao.strip()
                if salvar_glossario(termos_glossario): 
                    flash('Termo alterado com sucesso!', 'success')
                    return redirect(url_for('glossario_page'))
                else:
                    flash('Erro ao alterar o termo.', 'error')
        # Se houver erro ou aviso, renderiza o formulário novamente com os dados atuais
        return render_template('alterar_termo.html', page_name='glossario', termo_original={'termo': novo_termo_str, 'definicao': nova_definicao}, termo_id=termo_id)

    return render_template('alterar_termo.html', page_name='glossario', termo_original=termo_para_alterar, termo_id=termo_id)

@app.route('/glossario/eliminar/<int:termo_id>', methods=['POST'])
def eliminar_termo(termo_id):
    termos_glossario = carregar_glossario() 
    if 0 <= termo_id < len(termos_glossario):
        del termos_glossario[termo_id] 
        if salvar_glossario(termos_glossario): 
            flash('Termo eliminado com sucesso!', 'success')
        else:
            flash('Erro ao eliminar o termo.', 'error')
    else:
        flash('Termo não encontrado para eliminação.', 'error')
    return redirect(url_for('glossario_page'))

# --- ROTA PARA "TIRAR DÚVIDAS" ---
@app.route('/tirar-duvidas', methods=['GET', 'POST'])
def tirar_duvidas():
    resposta_formatada = None 
    pergunta_usuario = ""
    if request.method == 'POST':
        pergunta_usuario = request.form.get('pergunta')
        if pergunta_usuario:
            if GEMINI_AVAILABLE and gemini_model:
                try:
                    contexto_pergunta = (
                        "Você é um assistente virtual de um site sobre fundamentos de programação em Python e Flask. "
                        "Responda à seguinte pergunta do usuário de forma clara e concisa, "
                        "focando em conceitos de programação, Python ou Flask. "
                        "Se a pergunta for muito fora do escopo, informe educadamente.\n\n"
                        f"Pergunta do usuário: {pergunta_usuario}"
                    )
                    response = gemini_model.generate_content(contexto_pergunta)
                    resposta_formatada = response.text 
                    flash('Resposta gerada pela IA.', 'success')
                except Exception as e:
                    resposta_formatada = f"Ocorreu um erro ao contactar a IA: {e}. Usando resposta simulada."
                    print(f"ERRO API Gemini: {e}") 
                    resposta_formatada += "\n\n" + simular_resposta_gemini(pergunta_usuario) # Adiciona simulação
                    flash('Erro ao contactar a IA. Usando simulação.', 'error')
            else: # Simulação se API não disponível ou modelo não carregado
                resposta_formatada = simular_resposta_gemini(pergunta_usuario)
                flash_message = 'Pergunta processada (simulação - API não disponível/configurada).' if not GEMINI_AVAILABLE else 'Pergunta processada (simulação - modelo IA não inicializado).'
                flash(flash_message, 'info')
        else:
            flash('Por favor, insira uma pergunta.', 'warning')

    return render_template('tirar_duvidas.html', page_name='tirar_duvidas', resposta=resposta_formatada, pergunta_anterior=pergunta_usuario)

def simular_resposta_gemini(pergunta_usuario):
    pergunta_lower = pergunta_usuario.lower()
    if "python" in pergunta_lower:
        return f"Resposta simulada para '{pergunta_usuario}': Python é uma linguagem de programação poderosa e versátil. Para saber mais, consulte a documentação oficial ou as seções deste site."
    elif "flask" in pergunta_lower:
         return f"Resposta simulada para '{pergunta_usuario}': Flask é um microframework web para Python. É conhecido pela sua simplicidade."
    elif "o que é" in pergunta_lower and "api" in pergunta_lower:
        return f"Resposta simulada para '{pergunta_usuario}': Uma API (Application Programming Interface) é um conjunto de regras e protocolos que permite que diferentes softwares se comuniquem entre si."
    else:
        return f"Resposta simulada para '{pergunta_usuario}': Desculpe, não tenho informações sobre isso no momento. Tente perguntar sobre Python, Flask ou conceitos básicos de programação."

if __name__ == '__main__':
    if not os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, mode='w', encoding='utf-8', newline='') as file:
                # Opcional: Adicionar cabeçalho ou um termo inicial se desejar
                # csv_writer = csv.writer(file, delimiter=';')
                # csv_writer.writerow(['TermoExemplo', 'DefinicaoExemplo'])
                print(f"INFO: Arquivo {CSV_FILE} não encontrado. Um novo arquivo vazio foi criado.")
        except Exception as e:
            print(f"AVISO: Não foi possível criar o arquivo {CSV_FILE}: {e}")
    
    # Imprime o mapa de URLs para depuração (opcional)
    # with app.app_context():
    #     print("\n--- Mapa de URLs Registradas ---")
    #     print(app.url_map)
    #     print("---------------------------------\n")

    app.run(host='0.0.0.0', port=5000, debug=True)
