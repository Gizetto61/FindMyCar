import requests
import mysql.connector
import time

API_KEY = "yjysvl5k9_b0no62iow_jl7l2bn2t"

# Banco Railway
conn = mysql.connector.connect(
    host="switchyard.proxy.rlwy.net",
    port=41357,
    user="root",
    password="EHnlBexYxFZuogtSOZHuvNloklbjNFqt",
    database="railway"
)
cursor = conn.cursor()

# Criar tabela para armazenar dados gerais de carros
cursor.execute("""
CREATE TABLE IF NOT EXISTS carros_modelos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fabricante VARCHAR(50),
    modelo VARCHAR(100),
    ano INT,
    horsepower INT,
    preco VARCHAR(50),
    peso VARCHAR(50),
    tamanho VARCHAR(50),
    imagem TEXT,
    consumo_cidade VARCHAR(20),
    consumo_estrada VARCHAR(20)
)
""")

# 1. Pega todas as marcas
url_makes = f"https://api.carsxe.com/makes?key={API_KEY}"
res_makes = requests.get(url_makes)
makes = res_makes.json().get("makes", [])

for make in makes:
    fabricante = make.get("make_name")
    print(f"Processando marca: {fabricante}")

    # 2. Pega modelos da marca
    url_models = f"https://api.carsxe.com/models?key={API_KEY}&make={fabricante}"
    res_models = requests.get(url_models)
    models = res_models.json().get("models", [])

    for model_obj in models:
        modelo = model_obj.get("model_name")
        # 3. Vamos tentar obter anos disponíveis para esse modelo, se a API permitir
        # A CarsXE não tem endpoint direto de anos, então vamos tentar consultar specs para o modelo e anos genéricos

        anos_teste = [2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000]  # você pode ampliar essa lista

        for ano in anos_teste:
            print(f"  Consultando {fabricante} {modelo} {ano}")

            url_specs = f"https://api.carsxe.com/specs?key={API_KEY}&make={fabricante}&model={modelo}&year={ano}"
            res_specs = requests.get(url_specs)
            if res_specs.status_code != 200:
                print(f"    Sem dados para {modelo} {ano}")
                continue

            dados = res_specs.json()
            if "make" not in dados:
                print(f"    Dados insuficientes para {modelo} {ano}")
                continue

            horsepower = int(dados.get("specs", {}).get("horsepower", 0))
            preco = dados.get("price", {}).get("baseMsrp", "")
            peso = dados.get("specs", {}).get("curbWeight", "")
            tamanho = dados.get("specs", {}).get("overallLength", "")
            consumo_cidade = dados.get("specs", {}).get("fuelEconomyCity", "")
            consumo_estrada = dados.get("specs", {}).get("fuelEconomyHighway", "")
            imagem = dados.get("photoUrls", [None])[0] if dados.get("photoUrls") else ""

            # Inserir no banco
            cursor.execute("""
                INSERT INTO carros_modelos (
                    fabricante, modelo, ano, horsepower, preco, peso, tamanho, imagem, consumo_cidade, consumo_estrada
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (fabricante, modelo, ano, horsepower, preco, peso, tamanho, imagem, consumo_cidade, consumo_estrada))

            conn.commit()
            print(f"    Inserido: {fabricante} {modelo} {ano}")

            time.sleep(1.2)  # respeitar rate limit

cursor.close()
conn.close()
print("Finalizado!")
