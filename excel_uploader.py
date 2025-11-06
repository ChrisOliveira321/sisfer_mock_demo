# excel_uploader.py
import pandas as pd
import requests
import sys
import time

API = "http://127.0.0.1:5000"
USUARIO = "transp1"
SENHA = "senha123"
XLSX_FILE = "carregamentos.xlsx"

def login():
    r = requests.post(API + "/login", json={"usuario": USUARIO, "senha": SENHA})
    if r.status_code != 200:
        print("Falha no login:", r.status_code, r.text)
        sys.exit(1)
    return r.json()['token']

def enviar_linha(token, placa, produto, peso):
    headers = {"Authorization": "Bearer " + token}
    payload = {"placa": placa, "produto": produto, "peso": float(peso)}
    r = requests.post(API + "/carregamentos", json=payload, headers=headers)
    return r

def main():
    try:
        df = pd.read_excel(XLSX_FILE)
    except Exception as e:
        print("Erro lendo planilha:", e)
        sys.exit(1)

    # valida colunas mínimas
    expected = ["Placa", "Produto", "Peso"]
    for col in expected:
        if col not in df.columns:
            print(f"Planilha precisa ter a coluna '{col}'")
            sys.exit(1)

    token = login()
    print("Token obtido:", token)

    for idx, row in df.iterrows():
        placa = row['Placa']
        produto = row['Produto']
        peso = row['Peso']
        print(f"[{idx+1}/{len(df)}] Enviando: {placa} | {produto} | {peso}")
        r = enviar_linha(token, placa, produto, peso)
        if r.status_code == 200:
            print(" -> OK:", r.json())
        else:
            print(" -> Erro:", r.status_code, r.text)
        time.sleep(0.5)  # pequeno delay para demo

if __name__ == "__main__":
    main()
