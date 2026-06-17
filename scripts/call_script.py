import subprocess

ROOT = 'C:\\MV3\BPA003 - PAX Capital - SYSPAX\\03. Scripts Powershell\\INPUT_MANUAL'

def call_pwsh(file:str, param1:str = '', param2:str = ''):

    subprocess.run([
        'powershell',
        '-File',
        f'{ROOT}\\{file} {param1} {param2}'
    ])