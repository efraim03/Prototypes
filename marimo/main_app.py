import marimo

__generated_with = "0.23.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt

    return mo, pd, plt


@app.cell
def _(mo):
    file = mo.ui.file(label="📂 Upload CSV", filetypes=[".csv"])
    file
    return (file,)


@app.cell
def _(file, mo, pd):
    import io

    if file.value is None:
        mo.md("### Faça upload de um CSV para começar")
        df = None
    else:
        upload = file.value[0]          # pega o objeto
        file_bytes = upload.contents    # pega os bytes
        df = pd.read_csv(io.BytesIO(file_bytes))

    df
    return (df,)


@app.cell
def _(mo):
    col_input = mo.ui.text(
        label="Digite o nome da coluna numérica:",
        value="molecular_weight"
    )

    col_input
    return (col_input,)


@app.cell
def _(col_input, df, mo):
    slider = None
    col = col_input.value

    if df is not None and col in df.columns:
        slider = mo.ui.slider(
            start=float(df[col].min()),
            stop=float(df[col].max()),
            label=f"Filtrar por {col}"
        )

    slider, col
    return col, slider


@app.cell
def _(col, df, slider):
    _ = slider.value if slider is not None else None

    if df is not None:
        if slider is not None and col in df.columns:
            filtered_df = df[df[col] <= slider.value]
        else:
            filtered_df = df

    filtered_df.head(20).reset_index(drop=True)
    return


@app.cell
def _(col, df, plt, slider):
    _ = slider.value if slider is not None else None

    if df is not None and slider is not None and col in df.columns:
        _df_plot = df[df[col] <= slider.value]

        fig, ax = plt.subplots()
        ax.hist(_df_plot[col], bins=20)
        ax.set_title(f"Distribuição de {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Frequência")

    fig
    return


if __name__ == "__main__":
    app.run()
