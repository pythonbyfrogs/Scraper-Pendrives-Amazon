#Importações
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

#Acesso ao site
url = "https://www.amazon.com.br/s?k=pendrive"
try:
    sessao = requests.Session()

    headers = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language":"pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding":"gzip, deflate, br",
        "Connection":"keep-alive",
        "Upgrade-Insecure-Requests":"1"
}

#Entrada no site
    time.sleep(2)
    resposta = sessao.get("https://www.amazon.com.br/", headers=headers)
    time.sleep(2)

    resposta = sessao.get(url, headers=headers)
    time.sleep(2)

    if resposta.status_code != 200:
        print(f"Error at acessing {url}, Code: {resposta.status_code}")
except:
    print ("Error")

#Pegar os anuncios
time.sleep(2)
soup = BeautifulSoup(resposta.text, 'html.parser')
blocos_produtos = soup.find_all("div", attrs={"data-component-type":"s-search-result"})

lista_produtos = []

for bloco in blocos_produtos:
    try:
        #Titulo
        tag_titulo = bloco.find("h2", attrs={"class":"a-size-base-plus a-spacing-none a-color-base a-text-normal"})
        Produto = tag_titulo.text.strip() if tag_titulo else "Indisponível"

        #Procura o preço do produto
        tag_preco = bloco.find("span", attrs={"class":"a-price"})
        preco_sujo = tag_preco.text.strip() if tag_preco else "Indisponível"
        if "R$" in preco_sujo:
            preco = "R$" + preco_sujo.split("R$")[1].strip()
        else:
            preco = preco_sujo

        lista_produtos.append({"Produto": Produto, "Preço": preco})
        print(f"Produto: {Produto} | Preço: {preco}")

    except Exception:
        continue

#Criar DataFrame
if lista_produtos:
    df = pd.DataFrame(lista_produtos)
    df.to_csv("Pendrives_amazon.csv", index= False, encoding="utf-8")
    print("\n Planilha gerada com sucesso!")
else:
    print("\n Erro ao gerar a planilha ou coletar os produtos")