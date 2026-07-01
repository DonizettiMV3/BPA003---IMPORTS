import mysql.connector
from database.connection import create_connection

def Telefone_updateDados(nome_arquivo):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
                UPDATE tbl_dados_processos tdp 
                INNER JOIN tbl_input_processos tip 
                ON
                   tdp.processo_comunicacao = tip.numero_precatorio
                SET 
                   tdp.STATUS_SYSPAX = 'Concluido', tdp.DESCRICAO_SYSPAX='Telefone não cadastrado'
                WHERE
                    tdp.STATUS_SYSPAX ='Telefone' AND tip.nome_arquivo_importacao ='{nome_arquivo}'
                """)
        
    cursor.close()
    conn.close()