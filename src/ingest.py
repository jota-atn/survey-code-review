import pandas as pd
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Uso: python ingest.py <arquivo_csv_exportado_do_forms>")
    sys.exit(1)

infile = Path(sys.argv[1])
if not infile.exists():
    print(f"Arquivo não encontrado: {infile}")
    sys.exit(1)

df = pd.read_csv(infile)
out_path = Path("data/raw") / "responses.csv"
out_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out_path, index=False)
print(f"Arquivo salvo em: {out_path} ({df.shape[0]} linhas)")
