from get_process import get_syspax
from database.queries import select_arquivos


def main():
    while True:
        #Verifica arquivos pendentes
        get_syspax()

        #Verifica arquivo pendente - TELEFONES
        rows = ''
        rows = select_arquivos('Telefone')

        if len(rows):
            ...

        #Verifica arquivo pendente - NOTAS
        rows = ''
        rows = select_arquivos('Syspax - Processado')

        if len(rows):
            ...
        

        #Verifica arquivo pendente - Lemitti
        rows = ''
        rows = select_arquivos('Lemitti - Processado')

        if len(rows):
            ...


        #Verifica arquivo pendente - LEMMIT
        rows = ''
        rows = select_arquivos('Lemitti - Pendente')

        if len(rows):
            ...
        
        #Verifica arquivo pendente - IMPORT
        rows = ''
        rows = select_arquivos('Novo')

        if len(rows):
            ...





if __name__ == "__main__":
    main()