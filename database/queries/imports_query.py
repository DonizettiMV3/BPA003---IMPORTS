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

def imports_updateDuplicateProcess(hora, file_name):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
            UPDATE tbl_input_processos
            SET 
                status = 'Não importado',
                execucao_importacao = 'Existente fila Syspax',
                data_importacao = '{hora}'
            WHERE
                caminho_arquivo_importacao = '{file_name}'
                AND EXISTS (
                        SELECT 1
                        FROM tbl_dados_processos tdp
                            WHERE tbl_input_processos.numero_processo = tdp.NUMERO_PROCESSO
                            AND tbl_input_processos.nome_requerente = tdp.REQUERENTE
                            AND tbl_input_processos.numero_precatorio = tdp.processo_comunicacao
                            AND tbl_input_processos.documento_requerente = tdp.DOCUMENTO
                            AND tbl_input_processos.valor_espelho_principal = tdp.valor_solicitado
                            AND tbl_input_processos.sigla_tribunal=tdp.juizo_de_origem
                            AND tdp.status = 'IMPORTADO - Syspax'
                ) AND status='Lemitti - Pendente';
                """)
        
    cursor.close()
    conn.close()