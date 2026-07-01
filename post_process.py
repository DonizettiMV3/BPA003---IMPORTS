from scripts.call_script import call_pwsh
import database.queries.post_query as db
import database.queries.shared as sh
from datetime import datetime

def post_process():
        

    rows = sh.select_arquivos('Lemitti - Processado')

    for row in rows:
        #Setando variaveis
        id = row[0]
        id_syspax = row[1]
        file_name = row[2]
        date_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        
        #Chama script para mudar status no syspax
        call_pwsh('Syspax_UpdateStatus_Api.', f'"{id_syspax}"', f'"Cadastrando no Syspax"')

        #Atualiza status para duplicado caso requerente já exista na dados_processos
        db.Post_updateDuplicate(date_now)

        #Atualiza processos pendentes do arquivo para post
        sh.update_process(
            set=f"status = 'Post', data_processamento_syspax= '{date_now}'",
            condition=f"status ='Lemitti - Processado' AND nome_arquivo_importacao = '{file_name}'"
            )

        #Insere processos na dados_processos
        db.Post_InsertDadosProcessos(hora= date_now, id_arquivo=id, nome_arquivo= file_name)    
        
        #Verifica se dados foram inseridos
        verify_temp = db.Post_SelectDados(file_name)

        count = 0
        count = verify_temp[0]

        if count <= 0:
            #Dados não encontrados, setando arquivo como finalizado
            sh.update_arquivo(id= id, set = f"fim_processamento_syspax='{date_now}', status_processamento='Finalizado'")

        else: 
            #Executa script para post de processos
            call_pwsh('Syspax_Processos_Api.ps1', f'"{file_name}"')

            #Atualiza arquivo
            sh.update_arquivo(id = id,
                            set =  f"""status_processamento = 'Syspax - Processado', fim_processamento_syspax='{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', inicio_processamento_syspax = '{date_now}'""")

        #Atualiza arquivo no sysoax
        call_pwsh('Syspax_UpdateStatus_Api.', f'"{id_syspax}"', f'"Processando"')





