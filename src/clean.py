import pandas as pd
from pathlib import Path

rename_map = {
    "Você está atualmente matriculado no curso de Ciência da Computação na UFCG?":"matriculado",
    "Qual seu vínculo com o curso de Computação da UFCG?":"vinculo",
    "Você já participou de Code Reviews durante sua graduação?":"participou_role",
    "Com que frequência você participa de Code Reviews?":"freq_participa",
    "Você recebeu orientações ou treinamentos formais sobre como realizar Code Reviews?":"treinamento",
    "Já se sentiu desconfortável ou atacado(a) durante um Code Review?":"desconforto",
    "Você já presenciou comentários ríspidos ou mal interpretados em Code Reviews?":"comentarios_rispidos",
    "Você acredita que o jeito de dar feedback influencia diretamente no clima da equipe?":"feedback_influencia_clima",
    "Você já evitou revisar ou enviar código por medo de críticas negativas?":"evitou_por_medo",
    "Antes de responder um comentário que não gostou, você costuma “respirar fundo” ou pensar antes de responder?":"respira",
    "Você costuma considerar que o outro pode estar aprendendo ou inseguro antes de criticar um código?":"empatia",
    "Nos Code Reviews que você participa, a comunicação geralmente é clara e respeitosa?":"comunicacao_respeitosa",
    "Você já fez um comentário técnico que foi interpretado como pessoal, mesmo sem essa intenção?":"comentario_malinterpre",
    "Você já recebeu um feedback que te motivou a melhorar significativamente seu código?":"feedback_motivador",
    "Você sente que Code Reviews ajudam a melhorar suas habilidades de programação?":"ajuda_aprendizado",
    "Você sente que Code Reviews contribuem para um bom relacionamento dentro da equipe?":"contribui_relacionamento",
    "Você considera que a forma como o feedback é dado influencia sua motivação para contribuir no projeto?":"influencia_motivacao"
}

likert_frequencia = {
    'Nunca':1, 'Raramente':2, 'Às vezes':3, 'Frequentemente':4, 'Sempre':5
}
likert_acordo = {
    'Discordo totalmente':1, 'Discordo':2, 'Neutro':3, 'Concordo':4, 'Concordo totalmente':5
}

freq_cols = [
    'freq_participa','desconforto','comentarios_rispidos','evitou_por_medo',
    'respira','empatia','comunicacao_respeitosa','comentario_malinterpre','feedback_motivador'
]
acordo_cols = [
    'feedback_influencia_clima','ajuda_aprendizado','contribui_relacionamento','influencia_motivacao'
]

infile = Path("data/raw/responses.csv")
if not infile.exists():
    raise FileNotFoundError(f"Arquivo não encontrado: {infile}")

df = pd.read_csv(infile)
df = df.rename(columns=rename_map)

df = df[df['vinculo'].notna()]

for col in freq_cols:
    if col in df.columns:
        df[col] = df[col].map(likert_frequencia)

for col in acordo_cols:
    if col in df.columns:
        df[col] = df[col].map(likert_acordo)

df = df.drop_duplicates()

out_path = Path("data/processed/responses_clean.csv")
out_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out_path, index=False)
print(f"Arquivo processado salvo em: {out_path} ({df.shape[0]} linhas)")
