import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

infile = Path("data/processed/responses_clean.csv")
if not infile.exists():
    raise FileNotFoundError(f"Arquivo processado não encontrado: {infile}")

df = pd.read_csv(infile)

figs_path = Path("reports/figs")
figs_path.mkdir(parents=True, exist_ok=True)

for col in df.columns:
    if df[col].dtype in ['int64', 'float64']:
        plt.figure(figsize=(6,4))
        counts = df[col].value_counts().sort_index()
        plt.bar(counts.index, counts.values)
        plt.title(col)
        plt.xlabel("Escala")
        plt.ylabel("Contagem")
        plt.xticks(counts.index)
        plt.tight_layout()
        plt.savefig(figs_path / f"{col}_bar.png", dpi=150)
        plt.close()

numeric_df = df.select_dtypes(include=['int64', 'float64'])
if not numeric_df.empty:
    corr = numeric_df.corr(method='spearman')
    plt.figure(figsize=(10,8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Matriz de Correlação (Spearman)")
    plt.tight_layout()
    plt.savefig(figs_path / "correlacoes_heatmap.png", dpi=150)
    plt.close()

print(f"Gráficos gerados em: {figs_path}")