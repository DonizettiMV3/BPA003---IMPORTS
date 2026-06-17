from scripts.call_script import call_pwsh
from database.queries import select_arquivos

def get_syspax():
    #chama script para verificar se existe algum input pendente
    call_pwsh('Syspax_DownloadFiles_Api.ps1')

    #realizas select em input arquivos procurando status 'Novo'
    rows = select_arquivos('Novo')

    #Loop sobre dados retornados
    for row in rows:
        #Seta ID syspax
        id_syspax = row[1]
        
        #Chama script para alterar status no syspax
        call_pwsh('Syspax_UpdateStatus_Api.ps1', f'"{id_syspax}"', f'"Em Fila"')

if __name__ == "__main__":
    get_syspax()