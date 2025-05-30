from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
# Para a integração com a API do Gemini (exemplo)
import google.generativeai as genai 

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necessário para usar flash messages

# Configuração da API do Gemini (exemplo - substitua pela sua chave)
# Descomente e configure quando estiver pronto para integrar
GOOGLE_API_KEY = 'AIzaSyBSiM1b-XHivW5_dWep0mokQnC3M-T0nmQ'
genai.configure(api_key=GOOGLE_API_KEY)
# model = genai.GenerativeModel('gemini-pro') # Ou outro modelo apropriado

# Caminho para o arquivo CSV do glossário
CSV_FILE = 'bd_glossario.csv'

# --- INÍCIO DA LÓGICA DE PERSISTÊNCIA (ITEM 6) ---

# Função para LER o glossário do arquivo CSV
def carregar_glossario():
    glossario = []
    if not os.path.exists(CSV_FILE):
        # Se o arquivo não existir, pode optar por criá-lo aqui ou apenas retornar uma lista vazia.
        # open(CSV_FILE, 'w').close() # Cria um arquivo vazio se não existir
        return glossario
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8', newline='') as file:
            csv_reader = csv.reader(file, delimiter=';')
            for i, row in enumerate(csv_reader): # Adicionamos 'i' para ter um ID simples
                if len(row) == 2:
                    glossario.append({'id': i, 'termo': row[0].strip(), 'definicao': row[1].strip()})
                elif len(row) > 0 and not row[0].strip().startswith('#') and any(field.strip() for field in row):
                    print(f"Aviso: Linha {i+1} ignorada no CSV por formato inesperado: {row}")
    except FileNotFoundError:
        print(f"Erro: Arquivo {CSV_FILE} não encontrado.")
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
    return glossario

# Função para SALVAR (reescrever) o glossário no arquivo CSV
def salvar_glossario(glossario_data):
    try:
        with open(CSV_FILE, mode='w', encoding='utf-8', newline='') as file:
            csv_writer = csv.writer(file, delimiter=';')
            # Salvamos apenas o termo e a definição, o 'id' é gerado na leitura.
            for item in glossario_data:
                csv_writer.writerow([item['termo'], item['definicao']])
        return True # Indica sucesso
    except Exception as e:
        print(f"Erro ao salvar o arquivo CSV: {e}")
        return False # Indica falha
# --- FIM DA LÓGICA DE PERSISTÊNCIA (ITEM 6) ---

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


# --- ROTAS PARA OPERAÇÕES CRUD NO GLOSSÁRIO (ITEM 6) ---

# Rota para o glossário (LEITURA)
@app.route('/glossario')
def glossario_page():
    termos_glossario = carregar_glossario() # Lê do CSV
    return render_template('glossario.html', page_name='glossario', termos=termos_glossario)

# Rota para ADICIONAR termo ao glossário (ESCRITA)
@app.route('/glossario/adicionar', methods=['POST'])
def adicionar_termo():
    if request.method == 'POST':
        termo = request.form.get('termo')
        definicao = request.form.get('definicao')

        if not termo or not definicao:
            flash('Termo e definição são obrigatórios!', 'error')
            return redirect(url_for('glossario_page'))

        termos_glossario = carregar_glossario()
        
        if any(item['termo'].lower() == termo.lower() for item in termos_glossario):
            flash(f'O termo "{termo}" já existe no glossário.', 'warning')
            return redirect(url_for('glossario_page'))

        termos_glossario.append({'termo': termo.strip(), 'definicao': definicao.strip()})
        
        if salvar_glossario(termos_glossario): # Salva (reescreve) o CSV
            flash('Termo adicionado com sucesso!', 'success')
        else:
            flash('Erro ao salvar o termo.', 'error')
            
    return redirect(url_for('glossario_page'))

# Rota para ALTERAR termo (ATUALIZAÇÃO)
@app.route('/glossario/alterar/<int:termo_id>', methods=['GET', 'POST'])
def alterar_termo(termo_id):
    termos_glossario = carregar_glossario() # Lê do CSV
    termo_para_alterar = None
    
    # Encontra o termo pelo ID (que é o índice na lista ao carregar)
    # Este ID é temporário para a sessão de carregamento/salvamento
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
            return render_template('alterar_termo.html', page_name='glossario', termo_original=termo_para_alterar, termo_id=termo_id)

        # Verifica se o novo nome do termo (se alterado) já existe em outro item
        for i, item in enumerate(termos_glossario):
            if i != termo_id and item['termo'].lower() == novo_termo_str.lower():
                flash(f'O termo "{novo_termo_str}" já existe no glossário.', 'warning')
                return render_template('alterar_termo.html', page_name='glossario', termo_original=termo_para_alterar, termo_id=termo_id)

        # Atualiza o dicionário na lista
        termos_glossario[termo_id]['termo'] = novo_termo_str.strip()
        termos_glossario[termo_id]['definicao'] = nova_definicao.strip()
        
        if salvar_glossario(termos_glossario): # Salva (reescreve) o CSV
            flash('Termo alterado com sucesso!', 'success')
        else:
            flash('Erro ao alterar o termo.', 'error')
        return redirect(url_for('glossario_page'))

    # Método GET: exibir o formulário de alteração
    return render_template('alterar_termo.html', page_name='glossario', termo_original=termo_para_alterar, termo_id=termo_id)


# Rota para ELIMINAR termo (EXCLUSÃO)
@app.route('/glossario/eliminar/<int:termo_id>', methods=['POST'])
def eliminar_termo(termo_id):
    termos_glossario = carregar_glossario() # Lê do CSV
    
    if 0 <= termo_id < len(termos_glossario):
        del termos_glossario[termo_id] # Remove da lista
        if salvar_glossario(termos_glossario): # Salva (reescreve) o CSV
            flash('Termo eliminado com sucesso!', 'success')
        else:
            flash('Erro ao eliminar o termo.', 'error')
    else:
        flash('Termo não encontrado para eliminação.', 'error')
        
    return redirect(url_for('glossario_page'))
# --- FIM DAS ROTAS CRUD (ITEM 6) ---

# Rota para a página "Tirar Dúvidas"
@app.route('/tirar-duvidas', methods=['GET', 'POST'])
def tirar_duvidas():
    resposta_gemini = None
    pergunta_usuario = ""
    if request.method == 'POST':
        pergunta_usuario = request.form.get('pergunta')
        if pergunta_usuario:
            try:
                # --- INÍCIO DA SIMULAÇÃO DA CHAMADA À API DO GEMINI ---
                # No código real, você faria a chamada à API aqui.
                # Exemplo:
                # response = model.generate_content(pergunta_usuario)
                # resposta_gemini = response.text
                
                # Simulação:
                if "python" in pergunta_usuario.lower():
                    resposta_gemini = f"Resposta simulada para '{pergunta_usuario}': Python é uma linguagem de programação poderosa e versátil. Para saber mais, consulte a documentação oficial ou as seções deste site."
                elif "flask" in pergunta_usuario.lower():
                     resposta_gemini = f"Resposta simulada para '{pergunta_usuario}': Flask é um microframework web para Python. É conhecido pela sua simplicidade."
                else:
                    resposta_gemini = f"Resposta simulada para '{pergunta_usuario}': Desculpe, não tenho informações sobre isso no momento. Tente perguntar sobre Python ou Flask."
                # --- FIM DA SIMULAÇÃO ---
                flash('Pergunta processada (simulação).', 'info')
            except Exception as e:
                resposta_gemini = f"Ocorreu um erro ao processar sua pergunta: {e}"
                flash('Erro ao processar a pergunta.', 'error')
        else:
            flash('Por favor, insira uma pergunta.', 'warning')

    return render_template('tirar_duvidas.html', page_name='tirar_duvidas', resposta=resposta_gemini, pergunta_anterior=pergunta_usuario)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
