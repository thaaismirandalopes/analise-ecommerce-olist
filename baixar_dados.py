"""Baixa as tabelas públicas da Olist para a pasta dados/."""

import os
import urllib.request

ORIGEM = "https://raw.githubusercontent.com/olist/work-at-olist-data/master/datasets/"
PASTA = "dados"

ARQUIVOS = [
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_products_dataset.csv",
    "olist_order_payments_dataset.csv",
]

os.makedirs(PASTA, exist_ok=True)

for arquivo in ARQUIVOS:
    destino = os.path.join(PASTA, arquivo)
    if os.path.exists(destino):
        print("já existe:", arquivo)
        continue
    print("baixando:", arquivo)
    urllib.request.urlretrieve(ORIGEM + arquivo, destino)

print("Pronto. Os notebooks estão na pasta notebooks/")
