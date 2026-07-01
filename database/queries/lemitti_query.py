import mysql.connector
from database.connection import create_connection

def lemitti_updateTelefones(hora, nameFile):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
                UPDATE  tbl_input_processos tip 
                INNER JOIN tbl_telefones_participantes ttp 
                    ON tip.documento_requerente = ttp.documento_requerente 
                SET status='Lemitti - Processado',execucao_lemitti= 'Requerente já possui telefone(s).', data_processamento_lemitti = '{hora}'
                    WHERE tip.nome_arquivo_importacao LIKE '{nameFile}'
                """)
        
    cursor.close()
    conn.close()
