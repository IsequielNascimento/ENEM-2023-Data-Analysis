import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('./MICRODADOS_ENEM_2023.csv', encoding='latin-1', sep=",")



#Columns filters
selected_columns = ['NO_MUNICIPIO_PROVA', 'TP_ESCOLA', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
filtered_df = df[selected_columns]


# Filter by grades from Fortaleza, removal of null values ​​in grades and mapping of TP_ESCOLA values ​​for better readability

fortaleza_df = filtered_df[filtered_df['NO_MUNICIPIO_PROVA'] == 'Fortaleza']
fortaleza_df = fortaleza_df.dropna(subset=['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO'])
fortaleza_df['TP_ESCOLA'] = fortaleza_df['TP_ESCOLA'].replace({1: 'Não respondeu', 2: 'Pública', 3: 'Privada'})

fortaleza_df.head(10)

plt.figure(figsize=(12, 8))
areas_conhecimento = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']

# Renaming Knowledge Areas for the Chart
# Calculating the average of each area of ​​knowledge by type of school
grouped_data = fortaleza_df.groupby('TP_ESCOLA')[['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']].mean().reset_index()

grouped_data = grouped_data.rename(columns={
    "TP_ESCOLA": "Tipo de Escola",
    "NU_NOTA_CN": "Média Ciências da Natureza",
    "NU_NOTA_CH": "Média Ciências Humanas",
    "NU_NOTA_LC": "Média Linguagens e Códigos",
    "NU_NOTA_MT": "Média Matemática",
    "NU_NOTA_REDACAO": "Média Redação",
    "TP_ESCOLA": "Tipo de Escola"
})

grouped_data.attrs['title'] = "Médias de Notas por Tipo de Escola"
grouped_data


# Transforming DataFrame to long format for easier boxplot
long_df = fortaleza_df.melt(
    id_vars=['TP_ESCOLA'],
    value_vars=['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO'],
    var_name='Área de Conhecimento',
    value_name='Nota',
)
area_renames = {
    'NU_NOTA_CN': 'Ciências da Natureza',
    'NU_NOTA_CH': 'Ciências Humanas',
    'NU_NOTA_LC': 'Linguagens e Códigos',
    'NU_NOTA_MT': 'Matemática',
    'NU_NOTA_REDACAO': 'Redação',
}
long_df['Área de Conhecimento'] = long_df['Área de Conhecimento'].replace(area_renames)


#boxplot
plt.figure(figsize=(14, 8))
sns.boxplot(data=long_df, x='Área de Conhecimento', y='Nota', hue='TP_ESCOLA', palette='Set2')
plt.title('Distribuição das Notas por Área de Conhecimento e Tipo de Escola', fontsize=16)
plt.xlabel('Área de Conhecimento', fontsize=12)
plt.ylabel('Notas', fontsize=12)
plt.xticks(rotation=30, ha='right')
plt.legend(title='Tipo de Escola', fontsize=10, loc='upper right')
plt.tight_layout()
plt.show()