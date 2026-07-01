from scripts.call_script import call_pwsh
import database.queries.telefone_query as db
import database.queries.shared as sh
from datetime import datetime

rows = sh.select_arquivos('Telefone')

for row in rows:
    #Setando variaveis
    id = row[0]
    id_syspax = row[1]
    file_name = row[2]
    date_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    #Atualiza arquivo no sysoax
    call_pwsh('Syspax_UpdateStatus_Api.', f'"{id_syspax}"', f'"Importando Telefones"')

    #Executa script para cadastro de telefones
    call_pwsh('Syspax_Telefones_Api.ps1', f'"{file_name}"')

    #Atualiza status de processos sem telefone para 'concluido'
    sh.update_process(
        set = f" status = 'Concluido',data_processamento_telefones='{date_now}', execucao_telefones='Telefone não encontrado'",
        condition= f"status ='Telefone' AND nome_arquivo_importacao ='{file_name}' AND (execucao_lemitti='Documento Não Localizado' OR execucao_lemitti='Documento Inválido')"
    )

    #Atualiza dados processos
    db.Telefone_updateDados(nome_arquivo= file_name)

    #Atualiza arquivo para telefones
    sh.update_arquivo(id = id,
                          set =  f"""status_processamento = 'Finalizado',  fim_cadastro_telefones=''{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}',   inicio_cadastro_telefones= '{date_now}'""")
    
    #Atualiza arquivo no sysoax
    call_pwsh('Syspax_UpdateStatus_Api.', f'"{id_syspax}"', f'"Processando"')
    
