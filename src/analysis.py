import pandas as pd
from pathlib import Path
from scipy.stats import spearmanr

infile = Path("data/processed/responses_clean.csv")
if not infile.exists():
    raise FileNotFoundError(f"Arquivo processado não encontrado: {infile}")

df = pd.read_csv(infile)

print("\n=== Estatísticas Descritivas ===")
for col in df.columns:
    if df[col].dtype in ['int64', 'float64']:
        print(f"{col}: média={df[col].mean():.2f}, desvio={df[col].std():.2f}")

print("\n=== Correlações ===")
pairs = [
    ("empatia", "ajuda_aprendizado"),
    ("respira", "contribui_relacionamento"),
    ("feedback_influencia_clima", "influencia_motivacao")
]
for x, y in pairs:
    if x in df.columns and y in df.columns:
        r, p = spearmanr(df[x].dropna(), df[y].dropna())
        print(f"{x} ↔ {y}: Spearman r={r:.3f}, p={p:.4f}")
