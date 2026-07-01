import mysql.connector
from database.connection import create_connection

def select_arquivos(status):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
                SELECT id,
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

def update_arquivo(id,set):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
                UPDATE tbl_input_arquivos
                SET {set}
                WHERE id = {id}
                """)
    
    
    cursor.close()
    conn.close()

def update_process(condition, set):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
                UPDATE tbl_input_processos
                SET {set}
                WHERE {condition}
                """)
    
    
    cursor.close()
    conn.close()



if __name__ == "__main__":
    pass