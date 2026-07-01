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
        db.update_arquivo(id_syspax, f"status_processamento = 'Erro', data_importacao='{date_now}'")

    else:

        #Dados localizados na temp, inserindo na tabela de PROD
        db.imports_insertTemp(date_now, file_name, file_path)

        #Realiza update em processos já existentes da dados_processos
        db.imports_updateDuplicateProcess(date_now, file_name)







