from scripts.call_script import call_pwsh
from database.queries import select_arquivos,imports_deleteTemp, imports_selectTemp, update_arquivo
from datetime import datetime

rows = select_arquivos('Novo')

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
    imports_deleteTemp()

    #Executa scripts para imports
    call_pwsh('Import_File.ps1', f'"{file_path}"')

    #Verifica se linhas foram inseridas
    temp_verify = imports_selectTemp()

    count = 0
    count = temp_verify[0]

    if count <= 0:
        #Dados não encontrados, setando erro no arquivo
        update_arquivo(id_syspax, f"status_processamento = 'Erro', data_importacao='{date_now}'")

    else:

        ...



