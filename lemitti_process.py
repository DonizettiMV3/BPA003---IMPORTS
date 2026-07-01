from scripts.call_script import call_pwsh
import database.queries.lemitti_query as db
import database.queries.shared as sh
from datetime import datetime

def lemitti_process():

    rows = sh.select_arquivos('Lemitti - Pendente')

    for row in rows:
        #Setando variaveis
        id = row[0]
        id_syspax = row[1]
        file_name = row[2]
        date_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        #Chama script para mudar status no syspax
        call_pwsh('Syspax_UpdateStatus_Api.', f'"{id_syspax}"', f'"Buscando Telefones - Fornecedores"')

        #Atualiza status para processos com telefones já existentes
        db.lemitti_updateTelefones(hora=date_now, file_name = file_name)

        #Atualiza status para não importado caso não identifique numero de documento
        sh.update_process(
            set=f"status = 'Não importado', execucao_lemitti= 'Numero documento não identificado', data_processamento_lemitti = '{date_now}'",
            condition=f"caminho_arquivo_importacao ='{file_name}' AND (documento_requerente IS NULL OR LENGTH(documento_requerente)<=0) AND status='Lemitti - Pendente'")
        
        #Executa script para lemitti
        call_pwsh('Lemitti_Api.ps1',f'"{file_name}"')

        #Atualiza arquivo para lemitti - Processado
        sh.update_arquivo(
            set = f"status_processamento = 'Lemitti - Processado', fim_processamento_lemitti='{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', inicio_processamento_lemit='{date_now}'",
            id= id)

        #Atualiza status no syspax
        call_pwsh('Syspax_UpdateStatus_Api.', f'"{id_syspax}"', f'"Processando"')   
