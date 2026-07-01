from scripts.call_script import call_pwsh
import database.queries.imports_query as db
import database.queries.shared as sh
from datetime import datetime

rows = sh.select_arquivos('Novo')

for row in rows:
    #Setando variaveis
    id = row[0]
    id_syspax = row[1]
    file_name = row[2]
    file_path = row[3]
    date_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    #Chama script para mudar status no syspax
    call_pwsh('Syspax_UpdateStatus_Api.', f'"{id_syspax}"', f'"Validando Dados"')

    #Deleta tabela de input temp
    db.imports_deleteTemp()

    #Executa scripts para imports
    call_pwsh('Import_File.ps1', f'"{file_path}"')

    #Verifica se linhas foram inseridas
    temp_verify = db.imports_selectTemp()

    count = 0
    count = temp_verify[0]

    if count <= 0:
        #Dados não encontrados, setando erro no arquivo
        db.update_arquivo(id, f"status_processamento = 'Erro', data_importacao='{date_now}'")

    else:

        #Dados localizados na temp, inserindo na tabela de PROD
        db.imports_insertTemp(date_now, file_name, file_path)

        #Realiza update em processos já existentes da dados_processos
        db.imports_updateDuplicateProcess(date_now, file_name)

        #Realiza update em processos com nome de requerente maior que 255
        sh.update_process(condition=f"LENGTH(nome_requerente)>255 AND nome_arquivo_importacao ='{file_name}'", 
        set= f"status ='Não importado', execucao_importacao='Número de caracteres para nome de requerente acima do limite de API', data_importacao = '{date_now}'")

        #Realiza update em processos com campo faltando
        sh.update_process(condition=f""" ((data_autuacao IS NULL OR LENGTH(data_autuacao)<=0)
        OR (valor_espelho_principal IS NULL OR LENGTH(valor_espelho_principal)<=0)
        OR (nome_requerente IS NULL OR LENGTH(nome_requerente)<=0)
        OR (numero_processo IS NULL OR LENGTH(numero_processo)<=0)) 
        AND caminho_arquivo_importacao ='{file_name}' AND status='Lemitti - Pendente'""",
        set= f"status ='Não importado', execucao_importacao='Identificado campo(s) necessário(s) vazio(s)', data_importacao = '{date_now}'")

        #Realiza update de arquivo para Lemmit - Pendente
        sh.update_arquivo(id= id,
                          set= f"status_processamento = 'Lemitti - Pendente', data_importacao='{date_now}'")

    #Chama script para atualizar status no syspax
    call_pwsh('Syspax_UpdateStatus_Api.', f'"{id_syspax}"', f'"Processando"')


