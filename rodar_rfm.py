"""Roda a segmentação RFM no PostgreSQL, mostra o resumo e salva os gráficos."""

import matplotlib.pyplot as plt
import pandas as pd
import psycopg2

CINZA = "#BDBDBD"
PRETO = "#212121"

conexao = psycopg2.connect("")
cursor = conexao.cursor()

with open("sql/02_segmentacao_rfm.sql", encoding="utf-8") as arquivo_sql:
    cursor.execute(arquivo_sql.read())
conexao.commit()

with open("sql/03_resumo_segmentos.sql", encoding="utf-8") as arquivo_sql:
    cursor.execute(arquivo_sql.read())

colunas = [coluna[0] for coluna in cursor.description]
resumo = pd.DataFrame(cursor.fetchall(), columns=colunas)
resumo[["pct_clientes", "pct_receita"]] = resumo[["pct_clientes", "pct_receita"]].astype(float)

cursor.close()
conexao.close()

print(resumo.to_string(index=False))


def grafico_barras(coluna, destaque, titulo, rotulo_eixo, arquivo):
    dados = resumo.sort_values(coluna)
    cores = [PRETO if segmento in destaque else CINZA for segmento in dados["segmento"]]

    figura, eixo = plt.subplots(figsize=(8, 4))
    eixo.barh(dados["segmento"], dados[coluna], color=cores)
    eixo.spines["top"].set_visible(False)
    eixo.spines["right"].set_visible(False)
    eixo.set_title(titulo, loc="left", fontsize=13, fontweight="bold")
    eixo.set_xlabel(rotulo_eixo)
    for posicao, valor in enumerate(dados[coluna]):
        eixo.text(valor, posicao, f" {valor:.1f}%".replace(".", ","), va="center")
    eixo.set_xlim(0, dados[coluna].max() * 1.15)
    plt.tight_layout()
    plt.savefig("imagens/" + arquivo, dpi=150)
    plt.close()


ALTO_VALOR = ["Recentes de alto valor", "Em risco de alto valor"]

grafico_barras(
    coluna="pct_clientes",
    destaque=ALTO_VALOR,
    titulo="Os dois segmentos de alto valor somam 30% dos clientes",
    rotulo_eixo="% dos clientes",
    arquivo="07_rfm_clientes.png",
)

grafico_barras(
    coluna="pct_receita",
    destaque=ALTO_VALOR,
    titulo="Mas esses dois segmentos geram 57% da receita",
    rotulo_eixo="% da receita",
    arquivo="08_rfm_receita.png",
)

print("Gráficos salvos na pasta imagens/")
