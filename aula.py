from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

# para rodar o chrome em 2º plano
# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.headless = True 
# navegador = webdriver.Chrome(options=chrome_options)

navegador = webdriver.Chrome()
#pegar a cotação do dolar


#entrar no google
navegador.get("https://www.google.com.br/")

navegador.find_element('xpath','/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação dólar")
navegador.find_element('xpath','/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

cotacao_dolar = navegador.find_element('xpath', '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')

print(cotacao_dolar)

#pegar a cotação do euro
navegador.get("https://www.google.com.br/")

navegador.find_element('xpath','/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação euro")
navegador.find_element('xpath','/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

cotacao_euro = navegador.find_element('xpath', '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')
print(cotacao_euro)

# pegar cotação do ouro
navegador.get("https://www.melhorcambio.com/ouro-hoje")
cotacao_ouro = navegador.find_element('xpath', '//*[@id="comercial"]').get_attribute('value')
cotacao_ouro = cotacao_ouro.replace("," , ".")
print(cotacao_ouro)
# Importar dados e Atualizar a Base
tabela = pd.read_excel("Produtos.xlsx")


# Recalcular os preços

#atualizar os preços

tabela.loc[tabela["Moeda"] == "Dólar", "Cotação"] = float(cotacao_dolar)
tabela.loc[tabela["Moeda"] == "Ouro", "Cotação"] = float(cotacao_ouro)
tabela.loc[tabela["Moeda"] == "Euro", "Cotação"] = float(cotacao_euro)
print(tabela)

#preco de compra = cotação * preco original
tabela["Preço de Compra"] = tabela["Cotação"] * tabela["Preço Original"]
#preco de vendar = preco de compra *preco final
tabela["Preço de Venda"] = tabela["Preço de Compra"] * tabela["Margem"]
print(tabela)
# exportar a base atualizada
tabela.to_excel("Produtos Atualizado.xlsx")