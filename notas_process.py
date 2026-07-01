from scripts.call_script import call_pwsh
import database.queries.shared as sh
from datetime import datetime

def notas():

    rows = sh.select_arquivos('Syspax - Processado')

    for row in rows:
        #Setando variaveis
        id = row[0]
        id_syspax = row[1]
        file_name = row[2]
        date_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        #Atualiza arquivo no sysoax
        call_pwsh('Syspax_UpdateStatus_Api.', f'"{id_syspax}"', f'"Cadastrando Notas - Syspax"')

        #Executa script para Notas
        call_pwsh('Syspax_Notas_Api.ps1', f'"{file_name}"')

        #Atualiza arquivo para telefones
        sh.update_arquivo(id = id,
                            set =  f"""status_processamento = 'Telefone', fim_cadastro_notas='{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}',  inicio_cadastro_notas = '{date_now}'""")
        
        #Atualiza arquivo no sysoax
        call_pwsh('Syspax_UpdateStatus_Api.', f'"{id_syspax}"', f'"Processando"')   
    
