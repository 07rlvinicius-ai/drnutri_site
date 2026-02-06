"""
Módulo de rotas da aplicação
Contém todas as rotas e funções de manipulação de dados CSV
"""


from flask import render_template, request, redirect, url_for, flash, session
import os
from datetime import datetime
import uuid  # UC9: gerar id único para cada consulta
from functools import wraps


USUARIO_NUTRI = "nutri"
SENHA_NUTRI = "1234"

USUARIO_NUTRI = "vinicius"
SENHA_NUTRI = "Vinicius02"

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("nutri_logado"):
            flash("Acesso restrito. Faça login como nutricionista.", "error")
            return redirect(url_for("login", next=request.path))
        return func(*args, **kwargs)
    return wrapper

# Caminho para o arquivo CSV
CAMINHO_CSV = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'data',
    'agendamentos.csv'
)

# lista de status permitidos
STATUS_VALIDOS = ['Pendente', 'Confirmada', 'Cancelada', 'Concluída']


def _garantir_pasta_data():
    #Pasta/Data Existam
    pasta_data = os.path.dirname(CAMINHO_CSV)
    os.makedirs(pasta_data, exist_ok=True)


def _safe(valor):
    
    #Evita que vírgulas quebrem o CSV.
    
    return str(valor).replace(',', ' ').strip()


def _garantir_cabecalho():
    #CSV
    _garantir_pasta_data()

    if not os.path.exists(CAMINHO_CSV):
        with open(CAMINHO_CSV, 'w', encoding='utf-8') as arquivo:
            arquivo.write("id,nome,telefone,email,data,horario,tipo_consulta,status\n")
        return

    # Se existir mas estiver vazio
    if os.path.getsize(CAMINHO_CSV) == 0:
        with open(CAMINHO_CSV, 'w', encoding='utf-8') as arquivo:
            arquivo.write("id,nome,telefone,email,data,horario,tipo_consulta,status\n")


def ler_csv():
    #Le os dados CSV
    agendamentos = []

    if not os.path.exists(CAMINHO_CSV):
        return agendamentos

    with open(CAMINHO_CSV, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue


            lower = linha.lower()
            if lower.startswith('id,') or lower.startswith('nome,'):
                continue

            dados = linha.split(',')


            if len(dados) == 6:
                agendamento = {
                    'id': '',
                    'nome': dados[0],
                    'telefone': dados[1],
                    'email': dados[2],
                    'data': dados[3],
                    'horario': dados[4],
                    'tipo_consulta': dados[5],
                    'status': 'Pendente'
                }
                agendamentos.append(agendamento)


            elif len(dados) == 8:
                status_lido = dados[7] if dados[7] in STATUS_VALIDOS else 'Pendente'
                agendamento = {
                    'id': dados[0],
                    'nome': dados[1],
                    'telefone': dados[2],
                    'email': dados[3],
                    'data': dados[4],
                    'horario': dados[5],
                    'tipo_consulta': dados[6],
                    'status': status_lido
                }
                agendamentos.append(agendamento)

    return agendamentos


def escrever_csv(agendamento):
    #Escrever os Dados
    _garantir_cabecalho()

    # Garantir que todo agendamento novo tenha id e status
    if not agendamento.get('id'):
        agendamento['id'] = str(uuid.uuid4())

    if not agendamento.get('status') or agendamento['status'] not in STATUS_VALIDOS:
        agendamento['status'] = 'Pendente'

    linha = (
        f"{_safe(agendamento['id'])},"
        f"{_safe(agendamento['nome'])},"
        f"{_safe(agendamento['telefone'])},"
        f"{_safe(agendamento['email'])},"
        f"{_safe(agendamento['data'])},"
        f"{_safe(agendamento['horario'])},"
        f"{_safe(agendamento['tipo_consulta'])},"
        f"{_safe(agendamento['status'])}\n"
    )

    with open(CAMINHO_CSV, 'a', encoding='utf-8') as arquivo:
        arquivo.write(linha)


def reescrever_csv(agendamentos):
    #Reescrever o CSV com os Dados
    _garantir_pasta_data()

    with open(CAMINHO_CSV, 'w', encoding='utf-8') as arquivo:
        arquivo.write("id,nome,telefone,email,data,horario,tipo_consulta,status\n")

        for a in agendamentos:
            if not a.get('id'):
                a['id'] = str(uuid.uuid4())
            if not a.get('status') or a['status'] not in STATUS_VALIDOS:
                a['status'] = 'Pendente'

            linha = (
                f"{_safe(a['id'])},"
                f"{_safe(a['nome'])},"
                f"{_safe(a['telefone'])},"
                f"{_safe(a['email'])},"
                f"{_safe(a['data'])},"
                f"{_safe(a['horario'])},"
                f"{_safe(a['tipo_consulta'])},"
                f"{_safe(a['status'])}\n"
            )
            arquivo.write(linha)


def validar_formulario(dados):

    # Validar nome completo
    if not dados.get('nome') or len(dados['nome'].strip()) < 3:
        return False, "Nome completo deve ter pelo menos 3 caracteres"

    # Validar telefone
    if not dados.get('telefone') or len(dados['telefone'].strip()) < 10:
        return False, "Telefone deve ter pelo menos 10 dígitos"

    # Validar email
    if not dados.get('email') or '@' not in dados['email']:
        return False, "Email inválido"

    # Validar data
    if not dados.get('data'):
        return False, "Data é obrigatória"

    # Validar se a data não é no passado
    try:
        data_agendamento = datetime.strptime(dados['data'], '%Y-%m-%d')
        data_hoje = datetime.now()

        if data_agendamento.date() < data_hoje.date():
            return False, "Não é possível agendar consultas em datas passadas"
    except ValueError:
        return False, "Data inválida"

    # Validar horário
    if not dados.get('horario'):
        return False, "Horário é obrigatório"

    # Validar tipo de consulta
    tipos_validos = ['Nutrição Esportiva', 'Emagrecimento', 'Reeducação Alimentar']
    if not dados.get('tipo_consulta') or dados['tipo_consulta'] not in tipos_validos:
        return False, "Tipo de consulta inválido"

    # Se passou por todas as validações
    return True, ""


def registrar_rotas(app):
    
    #Função para registrar todas as rotas da aplicação
    

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/agendamento', methods=['GET', 'POST'])
    def agendamento():
        #GET e POST
        if request.method == 'POST':
            dados = {
                'nome': request.form.get('nome', '').strip(),
                'telefone': request.form.get('telefone', '').strip(),
                'email': request.form.get('email', '').strip(),
                'data': request.form.get('data', '').strip(),
                'horario': request.form.get('horario', '').strip(),
                'tipo_consulta': request.form.get('tipo_consulta', '').strip()
            }

            valido, mensagem_erro = validar_formulario(dados)

            if not valido:
                flash(mensagem_erro, 'error')
                return render_template('agendamento.html')

            # UC9: consulta nova começa com status "Pendente"
            dados['status'] = 'Pendente'

            try:
                escrever_csv(dados)
                flash(f'Agendamento realizado com sucesso para {dados["nome"]}!', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Erro ao salvar agendamento: {str(e)}', 'error')
                return render_template('agendamento.html')

        return render_template('agendamento.html')

    @app.route('/consultas')
    @login_required
    def consultas():
        #Ler dados e exibi a tabela
        try:
            agendamentos = ler_csv()
            return render_template(
                'consultas.html',
                agendamentos=agendamentos,
                status_validos=STATUS_VALIDOS
            )
        except Exception as e:
            flash(f'Erro ao carregar consultas: {str(e)}', 'error')
            return render_template(
                'consultas.html',
                agendamentos=[],
                status_validos=STATUS_VALIDOS
            )

    @app.route('/area-profissional')
    @login_required
    def area_profissional():
        #Na Área Profissional
        try:
            agendamentos = ler_csv()

            # Contadores por status
            totais_por_status = {s: 0 for s in STATUS_VALIDOS}
            for a in agendamentos:
                status = a.get('status') or 'Pendente'
                if status not in STATUS_VALIDOS:
                    status = 'Pendente'
                totais_por_status[status] += 1

            total = len(agendamentos)

            return render_template(
                'area_profissional.html',
                total=total,
                totais_por_status=totais_por_status
            )
        except Exception as e:
            flash(f'Erro ao carregar área profissional: {str(e)}', 'error')
            return render_template(
                'area_profissional.html',
                total=0,
                totais_por_status={s: 0 for s in STATUS_VALIDOS}
            )

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            usuario = request.form.get("usuario", "").strip()
            senha = request.form.get("senha", "").strip()
            destino = request.form.get("next") or url_for("area_profissional")

            if usuario == USUARIO_NUTRI and senha == SENHA_NUTRI:
                session["nutri_logado"] = True
                flash("Login realizado com sucesso!", "success")
                return redirect(destino)

            flash("Usuário ou senha inválidos.", "error")
            return render_template("login.html", next=request.form.get("next", ""))

        # GET
        return render_template("login.html", next=request.args.get("next", ""))


    @app.route("/logout")
    def logout():
        session.clear()
        flash("Você saiu do sistema.", "success")
        return redirect(url_for("index"))



    # Atualizar status da consulta
    @app.route('/consultas/<consulta_id>/status', methods=['POST'])
    @login_required
    def atualizar_status(consulta_id):

        novo_status = request.form.get('status', '').strip()

        if novo_status not in STATUS_VALIDOS:
            flash('Status inválido.', 'error')
            return redirect(url_for('consultas'))

        agendamentos = ler_csv()

        encontrou = False
        for a in agendamentos:
            # Se não tem id, não dá pra atualizar
            if a.get('id') == consulta_id:
                a['status'] = novo_status
                encontrou = True
                break

        if not encontrou:
            flash('Consulta não encontrada (talvez seja um registro antigo sem ID).', 'error')
            return redirect(url_for('consultas'))

        # Reescreve o CSV para persistir o status atualizado
        reescrever_csv(agendamentos)
        flash('Status atualizado com sucesso!', 'success')
        return redirect(url_for('consultas'))
