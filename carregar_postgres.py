"""Cria as tabelas no PostgreSQL e carrega os arquivos CSV da pasta dados/.

A conexão vem das variáveis de ambiente padrão do PostgreSQL:
PGHOST, PGPORT, PGUSER, PGPASSWORD e PGDATABASE.
"""

import psycopg2

PASTA = "dados/"

# A ordem importa: orders depende de customers, e order_items depende de orders.
ARQUIVOS = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
}

conexao = psycopg2.connect("")
cursor = conexao.cursor()

with open("sql/01_criar_tabelas.sql", encoding="utf-8") as arquivo_sql:
    cursor.execute(arquivo_sql.read())

for tabela, nome_arquivo in ARQUIVOS.items():
    with open(PASTA + nome_arquivo, encoding="utf-8") as arquivo_csv:
        cursor.copy_expert(f"COPY {tabela} FROM STDIN WITH (FORMAT csv, HEADER true)", arquivo_csv)
    cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
    print(f"{tabela}: {cursor.fetchone()[0]} linhas carregadas")

conexao.commit()
cursor.close()
conexao.close()
