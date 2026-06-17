import mysql.connector
from connection import create_connection

def select_arquivos(status):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
                SELECT 
                    id_arquivo_syspax,
                    nome_arquivo,
                    caminho_arquivo
                FROM tbl_input_arquivos
                WHERE status_processamento = '{status}'
                """)
    
    data = cursor.fetchall()
    
    cursor.close()
    conn.close()


    return data


if __name__ == "__main__":
    pass