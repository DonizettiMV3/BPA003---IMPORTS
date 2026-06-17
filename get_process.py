from scripts.call_script import call_pwsh

def get_syspax():
    #chama script para verificar se existe algum input pendente
    call_pwsh('Syspax_DownloadFiles_Api')


if __name__ == "__main__":
    get_syspax()