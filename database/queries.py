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

if __name__ == "__main__":
    pass