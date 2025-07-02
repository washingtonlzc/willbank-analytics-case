import os
import pandas as pd
import subprocess
import sys

silver_path = 'data/silver/'
silver_file = silver_path + 'silver_pix_transacoes.csv'
pipeline_script = 'scripts/silver_transform.py'

def verificar_colunas():
    if not os.path.exists(silver_file):
        print(f"Arquivo {silver_file} não encontrado.")
        return False
    
    df = pd.read_csv(silver_file)
    colunas_necessarias = ['birth_date', 'uf']
    faltando = [col for col in colunas_necessarias if col not in df.columns]
    
    if faltando:
        print(f"Colunas faltando no arquivo {silver_file}: {faltando}")
        return False
    
    print(f"Todas as colunas necessárias estão presentes no arquivo {silver_file}.")
    return True

def rodar_pipeline():
    # Caminho absoluto para o Python do venv
    venv_python = os.path.join(os.getcwd(), '.venv', 'Scripts', 'python.exe')
    print(f"Usando Python do venv: {venv_python}")

    resultado = subprocess.run([venv_python, pipeline_script], capture_output=True, text=True)
    print(resultado.stdout)
    if resultado.returncode != 0:
        print("Erro ao executar o pipeline silver_transform.py:")
        print(resultado.stderr)
        return False
    return True

if __name__ == '__main__':
    if not verificar_colunas():
        if not rodar_pipeline():
            print("Pipeline falhou, verifique os erros.")
        else:
            print("Pipeline executado com sucesso. Refaça a verificação se desejar.")
    else:
        print("Arquivo pronto para uso.")
