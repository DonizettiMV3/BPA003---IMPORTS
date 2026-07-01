import mysql.connector
from database.connection import create_connection

def imports_deleteTemp():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
                DELETE FROM tbl_input_processos_temp
                """)
        
    cursor.close()
    conn.close()


def imports_selectTemp():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
                SELECT COUNT(id) FROM tbl_input_processos_temp
                """)
    
    data = cursor.fetchall()
    
    cursor.close()
    conn.close()


    return data

def imports_insertTemp(hora,file_name,file_path):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        INSERT INTO tbl_input_processos (
                numero_precatorio,
                tipo_processo,
                sigla_tribunal,
                data_autuacao,
                assunto,
                vara,
                sigla_uf,
                nome_requerente,
                nome_requerido,
                documento_requerente,
                processos_originarios,
                numero_processo,
                advogados,
                valor_espelho_principal,
                data_base_valor_espelho_principal,
                valor_juros,
                valor_pps,
                valor_total,
                link_espelho,
                status,
                data_importacao,
                execucao_importacao,
                nome_arquivo_importacao,
                caminho_arquivo_importacao
    )
        SELECT
                numero_precatorio,
                tipo_processo,
                sigla_tribunal,
                data_autuacao,
                assunto,
                vara,
                sigla_uf,
                nome_requerente,
                nome_requerido,
                documento_requerente,
                processos_originarios,
                numero_processo,
                advogados,
                valor_espelho_principal,
                data_base_valor_espelho_principal,
                valor_juros,
                valor_pps,
                valor_total,
                link_espelho,
                'Lemitti - Pendente',
                '{hora}',
                'Processo importado com sucesso!',
                '{file_name}',
                '{file_path}'
	FROM tbl_input_processos_temp tipt;
                """)
        
    cursor.close()
    conn.close()