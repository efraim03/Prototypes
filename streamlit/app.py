import streamlit as st
import pandas as pd
import altair as alt

# Nome da página e ícone
st.set_page_config(page_title="BioSensIA", page_icon="🧬")

# Título e descrição da aplicação
st.markdown("""
            
# Bem vindo ao BioSensIA!
### Este é um protótipo de aplicação para um sistema de prospecção de bioativos para biossensores enzimáticos.
 """)

# Upload de arquivo para análise
file = st.file_uploader("Faça upload do seu conjunto de dados", type=["csv", "xlsx"])

#verifica se teve upload de arquivo
if file:

    #leitura do arquivo
    reader = pd.read_csv(file)

    #expandir para mostrar os dados brutos na forma de tabela, sem o índice
    exp = st.expander("Dados Brutos")
    exp.dataframe(reader, hide_index=True)

    #define o que é bioativo e o que não é, e coloca em expander
    bioatividade = reader["bioactivity"].value_counts()
    bioativas = reader[reader["bioactivity"] == 1]
    nao_bioativas = reader[reader["bioactivity"] == 0]
    exp2 = st.expander("Distribuição de Bioatividade")
    exp2.write(bioatividade)

    #tabelas de bioativos e não bioativos em abas e retira a coluna de bioatividade para não poluir a visualização
    tab_1, tab_2 = exp2.tabs(["Bioativas", "Não Bioativas"])
    with tab_1:
        bioativas_view = bioativas.drop(columns=["bioactivity"])
        st.dataframe(bioativas_view, hide_index=True)
    with tab_2:
        nao_bioativas_view = nao_bioativas.drop(columns=["bioactivity"])
        st.dataframe(nao_bioativas_view, hide_index=True)

    #definição de classe bioatividade para o gráfico
    plot_df = reader.copy()
    plot_df["classe"] = plot_df["bioactivity"].map({
        1: "Bioativa",
        0: "Não Bioativa"
    })

    #gráfico de logP x peso molecular, colorido por classe
    exp3 = st.expander("Relação LogP x Peso Molecular")
    grafico = alt.Chart(plot_df).mark_circle(size=80).encode(
        x=alt.X(
            "molecular_weight",
            scale=alt.Scale(padding=0),
            title="Peso Molecular"
        ),
        y=alt.Y(
            "logP",
            scale=alt.Scale(padding=0),
            title="logP"
        ),
        color=alt.Color(
            "classe",
            scale=alt.Scale(
                domain=["Bioativa", "Não Bioativa"],
                range=["blue", "red"]
            ),
            legend=alt.Legend(title="Classe")
        ),

        #ferramenta de tooltip para mostrar detalhes da molécula ao passar o mouse
        tooltip=[
            alt.Tooltip("molecule_id", title="Molécula"),
            alt.Tooltip("molecular_weight", title="Peso Molecular"),
            alt.Tooltip("logP", title="logP")
        ]
    )

    #tornar o gráfico interativo para permitir zoom e pan
    grafico_interativo = grafico.interactive()

    #coloca o gráfico interativo no expander com largura total do container
    exp3.altair_chart(grafico_interativo, use_container_width=True)