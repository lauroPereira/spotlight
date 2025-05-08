import os
import sys
import zipfile
import requests
import pandas as pd
import json
import re

# Sanitiza nome de arquivo
def limpar_nome(nome):
    return re.sub(r"[^a-zA-Z0-9]", "_", nome.strip().lower())

# Verifica argumento
if len(sys.argv) < 2:
    print("Uso: python ingest_consumidor_gov.py <nome_da_empresa>")
    sys.exit(1)

empresa = sys.argv[1]
nome_arquivo = limpar_nome(empresa)
url = "https://dados.mj.gov.br/dataset/0182f1bf-e73d-42b1-ae8c-fa94d9ce9451/resource/65706bcd-80ab-4231-a7ef-9e329420f001/download/basecompleta2025-03.zip"
zip_path = "data/basecompleta2025-03.zip"
csv_filename = "base_completa_2025-03.csv"
output_json = f"data/consumidor_{nome_arquivo}.json"

# Baixa o zip se ainda não existir
os.makedirs("data", exist_ok=True)
if not os.path.exists(zip_path):
    r = requests.get(url)
    with open(zip_path, "wb") as f:
        f.write(r.content)

# Extrai CSV
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extract(csv_filename, path="data")

# Lê CSV e filtra por empresa
df = pd.read_csv(f"data/{csv_filename}", sep=";", encoding="utf-8")
if "Nome Fantasia" not in df.columns or "Problema" not in df.columns:
    print("Colunas necessárias não encontradas no CSV.")
    sys.exit(1)

filtro = df["Nome Fantasia"].str.lower().str.contains(empresa.lower(), na=False)
reclamacoes = df.loc[filtro, "Problema"].dropna().astype(str).tolist()

# Salva JSON
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(reclamacoes, f, ensure_ascii=False, indent=2)

print(f"{len(reclamacoes)} reclamações salvas em {output_json}")
sys.exit(0)