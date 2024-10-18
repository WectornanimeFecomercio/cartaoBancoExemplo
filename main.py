from dotenv import load_dotenv
import sys, os, time
import itertools, threading
import getpass
import pyodbc
import uuid

load_dotenv()

keep_running = True

def infinite_progress_bar():
    global keep_running
    spinner = itertools.cycle(['-', '\\', '|', '/'])
    
    while keep_running:
        sys.stdout.write(f'\r{next(spinner)}')
        sys.stdout.flush()
        time.sleep(0.1)
    
    sys.stdout.write('\r')
    sys.stdout.flush()

def start_progress_bar():
    global keep_running
    keep_running = True
    progress_thread = threading.Thread(target=infinite_progress_bar)
    progress_thread.start()
    return progress_thread

def stop_progress_bar():
    global keep_running
    keep_running = False

# Defina os parâmetros de conexão
server = os.getenv('SERVER')
database = os.getenv('DATABASE')
username = os.getenv('USERNAMEDB')
password = str(os.getenv('PASSWORD'))

while len(password) == 0 or password == 'None':
    password = getpass.getpass("Digite a senha do banco: ")

connection_string = (
    'DRIVER={SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password}'
)

sqlCommandList = [
    f"""
		INSERT INTO dbo.ESTADO_CIVIL (CODIGO, DESCRICAO)
		VALUES
		('{str(uuid.uuid4())}', 'Solteiro(a)'),
		('{str(uuid.uuid4())}', 'Casado(a)'),
		('{str(uuid.uuid4())}', 'Viuvo(a)'),
		('{str(uuid.uuid4())}', 'Divorciado(a)'),
		('{str(uuid.uuid4())}', 'Separado(a)');
	""",
    f"""
		INSERT INTO dbo.CONTATO_TIPO (CODIGO, TIPO)
		VALUES
		('{str(uuid.uuid4())}', 'EMAIL'),
		('{str(uuid.uuid4())}', 'TELEFONE'),
		('{str(uuid.uuid4())}', 'CELULAR');
	""",
    f"""
        INSERT INTO dbo.TIPO (CODIGO, TIPO)
        VALUES
        ('{str(uuid.uuid4())}', 'TITULAR'),
        ('{str(uuid.uuid4())}', 'DEPENDENTE'),
        ('{str(uuid.uuid4())}', 'REPRESENTANDE'),
        ('{str(uuid.uuid4())}', 'AMIGO DO CARTÃO');
    """,
    f"""
        INSERT INTO dbo.EMPRESA_PARCERIA (CODIGO, EMPRESA)
        VALUES
        ('{str(uuid.uuid4())}', 'FECOMÉRCIO'),
        ('{str(uuid.uuid4())}', 'SENAC'),
        ('{str(uuid.uuid4())}', 'SESC'),
        ('{str(uuid.uuid4())}', 'SINDCOM JABOATÃO'),
        ('{str(uuid.uuid4())}', 'SINDILOJAS CARUARU');
    """,
    f"""
        INSERT INTO dbo.GRAU_PARENTESCO (CODIGO, DESCRICAO)
        VALUES
        ('{str(uuid.uuid4())}', 'CÔNJUGE/COMPANHEIRO(A)'),
        ('{str(uuid.uuid4())}', 'FILHO(A)/ENTEADO(A)'),
        ('{str(uuid.uuid4())}', 'MÃE/MADRASTA'),
        ('{str(uuid.uuid4())}', 'PAI/PADRASTO');
    """,
    f"""
        INSERT INTO dbo.SITUACAO (CODIGO, DESCRICAO)
        VALUES
        ('{str(uuid.uuid4())}', 'AGUARDANDO PAGAMENTO'),
        ('{str(uuid.uuid4())}', 'ATIVO'),
        ('{str(uuid.uuid4())}', 'INATIVO'),
        ('{str(uuid.uuid4())}', 'NÃO POSSUI INTERESSE'),
        ('{str(uuid.uuid4())}', 'EXPIRADO');
    """,
    f"""
        INSERT INTO dbo.SOLICITACAO_STATUS (CODIGO, DESCRICAO)
        VALUES
        ('{str(uuid.uuid4())}', 'ABERTO'),
        ('{str(uuid.uuid4())}', 'EM ANÁLISE'),
        ('{str(uuid.uuid4())}', 'ACEITO'),
        ('{str(uuid.uuid4())}', 'CANCELADO'),
        ('{str(uuid.uuid4())}', 'ENTREGUE'),
        ('{str(uuid.uuid4())}', 'RECUSADO');
    """,
    f"""
        INSERT INTO dbo.PONTO_VALOR (CODIGO, DESCRICAO, VALOR)
        VALUES
        ('{str(uuid.uuid4())}', 'VALOR POR CADA PONTO', 1 );
    """,
    f"""
        INSERT INTO dbo.PERFIL (CODIGO, DESCRICAO)
        VALUES
        ('{str(uuid.uuid4())}', 'ADMINISTRADOR'),
        ('{str(uuid.uuid4())}', 'CADASTRO DE USUARIO'),
        ('{str(uuid.uuid4())}', 'ATENDIMENTO'),
        ('{str(uuid.uuid4())}', 'FINANCEIRO'),
        ('{str(uuid.uuid4())}', 'API');
    """,
    f"""
        INSERT INTO dbo.PREMIOS (CODIGO, DESCRICAO, QTD_PONTOS, URL_TERMOS)
        VALUES
        ('{str(uuid.uuid4())}', 'SESC LAZER', '10', 'https://www.cartaodoempresario.com.br/assets/termos/01-05-pontos-sesc-lazer.pdf'),
        ('{str(uuid.uuid4())}', 'HOTEL SESC', '10', 'https://www.cartaodoempresario.com.br/assets/termos/02-10-pontos-hotel-sesc.pdf'),
        ('{str(uuid.uuid4())}', 'ESCOVA SECADORA', '15', 'https://www.cartaodoempresario.com.br/assets/termos/17-15-pontos-escova.pdf'),
        ('{str(uuid.uuid4())}', 'FONE DE OUVIDO BLUETOOTH', '15', 'https://www.cartaodoempresario.com.br/assets/termos/18-15-pontos-fone.pdf'),
        ('{str(uuid.uuid4())}', 'BARBEADOR PHILLIPS', '15', 'https://www.cartaodoempresario.com.br/assets/termos/19-15-pontos-barbeador.pdf'),
        ('{str(uuid.uuid4())}', 'VENTILADOR', '15', 'https://www.cartaodoempresario.com.br/assets/termos/20-15-pontos-ventilador.pdf'),
        ('{str(uuid.uuid4())}', 'DIA DE BELEZA', '20', 'https://www.cartaodoempresario.com.br/assets/termos/04-25-pontos-salao.pdf'),
        ('{str(uuid.uuid4())}', 'FRITADEIRA ELÉTRICA SEM ÓLEO', '20', 'https://www.cartaodoempresario.com.br/assets/termos/16-20-pontos-fritadeira.pdf'),
        ('{str(uuid.uuid4())}', 'ASSISTENTE VIRTUAL ALEXA', '35', 'https://www.cartaodoempresario.com.br/assets/termos/03-15-pontos-alexa.pdf'),
        ('{str(uuid.uuid4())}', 'CAIXA DE SOM JBL', '35', 'https://www.cartaodoempresario.com.br/assets/termos/05-252-pontos-flip.pdf'),
        ('{str(uuid.uuid4())}', 'BICICLETA', '40', 'https://www.cartaodoempresario.com.br/assets/termos/08-40-pontos-bicicleta.pdf'),
        ('{str(uuid.uuid4())}', 'HOSPEDAGEM FIM DE SEMANA - HOTEL SESC GARANHUNS, GUADALUPE OU TRIUNFO', '45', 'https://www.cartaodoempresario.com.br/assets/termos/   06-20-pontos-hotel-sesc.pdf'),
        ('{str(uuid.uuid4())}', 'HOSPEDAGEM DE UMA SEMANA - HOTEL SESC, GARANHUNS OU TRIUNFO', '50', 'https://www.cartaodoempresario.com.br/assets/termos/ 09-50-pontos-hotel-sesc.pdf'),
        ('{str(uuid.uuid4())}', 'UM SEMESTRE DE AULAS NO CURSO DE IDIOMAS DO SENAC PERNAMBUCO', '90', 'https://www.cartaodoempresario.com.br/assets/termos/    07-30-pontos-ingles-senac.pdf'),
        ('{str(uuid.uuid4())}', 'HOSPEDAGEM DE FINAL DE SEMANA - PORTAL DE GRAVATÁ', '90', 'https://www.cartaodoempresario.com.br/assets/termos/   10-110-pontos-portal-gravata.pdf'),
        ('{str(uuid.uuid4())}', 'SMARTWATCH SAMSUNG GALAXYWATCH4 OU SIMILAR', '100', 'https://www.cartaodoempresario.com.br/assets/termos/11-110-pontos-smartwatch.pdf'),
        ('{str(uuid.uuid4())}', 'SMARTTV LED 43"', '140', 'https://www.cartaodoempresario.com.br/assets/termos/12-140-pontos-tv.pdf'),
        ('{str(uuid.uuid4())}', 'NOTEBOOK DELL OU DE MARCA SIMILAR 14" CORE I3', '175', 'https://www.cartaodoempresario.com.br/assets/termos/13-160-pontos-notebook.   pdf'),
        ('{str(uuid.uuid4())}', 'APARELHO CELULAR APPLE IPHONE 14 128GB', '250', 'https://www.cartaodoempresario.com.br/assets/termos/14-200-pontos-iphone.pdf'),
        ('{str(uuid.uuid4())}', 'MOTO HONDA CG 160 START', '800', 'https://www.cartaodoempresario.com.br/assets/termos/15-500-pontos-motocicleta.pdf');
    """,
    f"""
        INSERT INTO CARTAO_NOVO.DBO.TERMOS  (CODIGO, TERMO)
        VALUES 
        ('{str(uuid.uuid4())}', 'DECLARO A VERACIDADE E RESPONSABILIDADE PELAS INFORMAÇÕES FORNECIDAS E CONCORDO COM OS  TERMOS DE USO E CONDIÇÕES DE CONTRATAÇÃO DO   CARTÃO DO EMPRESÁRIO E CONCORDO COM O  REGULAMENTO DO CARTÃO DO EMPRESÁRIO.'),
        ('{str(uuid.uuid4())}', 'CONCORDO COM A POLÍTICA DE PRIVACIDADE'),
        ('{str(uuid.uuid4())}', 'CONCORDO COM O COMPARTILHAMENTO DOS MEUS DADOS PESSOAIS E EMPRESARIAIS COM O SESC, SENAC E AS EMPRESAS PARCEIRAS DO CARTÃO DO EMPRESÁRIO.'),
        ('{str(uuid.uuid4())}', 'DECLARO QUE LI E ACEITO O REGULAMENTO DO PROGRAMA AMIGO DO CARTÃO DO EMPRESÁRIO DA FECOMÉRCIO PE.')
    """,
    f"""
        INSERT INTO VALORES(DESCRICAO, VALOR)
        VALUES
        ('VALOR TITULAR','269.1'),
        ('VALOR TITULAR','149.5'),
        ('VALOR TITULAR','150'),
        ('VALOR TITULAR','179.4'),
        ('VALOR TITULAR','149.9'),
        ('VALOR TITULAR','250'),
        ('VALOR TITULAR','209.3');
    """,
    f"""
        INSERT INTO VALORES(DESCRICAO, VALOR)
        VALUES 
        ('VALOR DEPENDENTE','39.9'),
        ('VALOR DEPENDENTE','14.9');
    """,
    f"""
        INSERT INTO VALORES(DESCRICAO, VALOR)
        VALUES
        ('VALOR RENOVAÇÃO','149.5'),
        ('VALOR RENOVAÇÃO','149.9'),
        ('VALOR RENOVAÇÃO','179.4'),
        ('VALOR RENOVAÇÃO','269.1'),
        ('VALOR RENOVAÇÃO','299');
    """,
    f"""
        INSERT INTO VALORES(DESCRICAO, VALOR)
        VALUES
        ('VALOR RENOVAÇÃO DEPENDENTE','39.9')
    """
]

try:
    print("Tentando se conectar com o banco de dados")
    progress_thread = start_progress_bar()
    conn = pyodbc.connect(connection_string)
    stop_progress_bar()
    progress_thread.join()
    print("Conexão bem-sucedida!")

    try:
        cursor = conn.cursor()
        for command in sqlCommandList:
            cursor.execute(command)

            percent = (sqlCommandList.index(command) + 1) / len(sqlCommandList)
            bar = '#' * int(50 * percent) + '-' * (50 - int(50 * percent))

            sys.stdout.write(f'\r[{bar}] {int(percent * 100)}%')
            sys.stdout.flush()
            time.sleep(0.05)
        conn.commit()
    except Exception as e:
        sys.stdout.write('\r\n')
        print("Erro ao executar SQL")
        conn.rollback()
    finally:
        conn.close()
except Exception as e:
    stop_progress_bar()
    progress_thread.join()
    print(f"Erro ao conectar ao banco de dados: \n{e}")
