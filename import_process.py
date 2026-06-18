from scripts.call_script import call_pwsh
from database.queries import select_arquivos

rows = select_arquivos('Novo')

for row in rows:
    #Setando variaveis
    id = row[0]
    id_syspax = row[1]
    file_name = row[2]
    path_name = row[3]

    #Chama script para mudar status no syspax
    call_pwsh('Syspax_UpdateStatus_Api.', f'"{id_syspax}"', f'"Validando Dados"')

    


