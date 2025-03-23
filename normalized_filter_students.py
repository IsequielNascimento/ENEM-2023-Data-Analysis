import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_student_counts(file_path):
    """
   Returns the total number of students in private, public and non-respondent schools in Fortaleza.

Parameters:
file_path (str): Path to the CSV file containing the ENEM microdata.

Returns:
dict: A dictionary with the total number of students by school type.
    """
    # Leitura do arquivo CSV
    df = pd.read_csv(file_path, encoding='latin-1', sep=",")

    # Seleção e filtro das colunas necessárias
    selected_columns = ['NO_MUNICIPIO_PROVA', 'TP_ESCOLA', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
    filtered_df = df[selected_columns]

    # Filtrando apenas os dados de Fortaleza
    fortaleza_df = filtered_df[filtered_df['NO_MUNICIPIO_PROVA'] == 'Fortaleza']

    # Mapeando os valores de TP_ESCOLA para maior legibilidade
    fortaleza_df['TP_ESCOLA'] = fortaleza_df['TP_ESCOLA'].replace({1: 'Não respondeu', 2: 'Pública', 3: 'Privada'})

    return fortaleza_df

def calculate_normalized_means(fortaleza_df):
    """
  Calculates the normalized averages of student grades by school type in Fortaleza.

Parameters:
fortaleza_df (DataFrame): Filtered DataFrame containing data from Fortaleza.

Returns:
DataFrame: DataFrame with the normalized averages by school type.  """
    # Calculando as médias por tipo de escola
    grouped_means = fortaleza_df.groupby('TP_ESCOLA')[['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']].mean()

    # Normalizando as médias pelo total de alunos por tipo de escola
    counts = fortaleza_df['TP_ESCOLA'].value_counts()
    normalized_means = grouped_means.divide(counts, axis=0)

    return normalized_means.reset_index()

def plot_normalized_means(normalized_means):
    """
  Plots a graph comparing the normalized means of grades by school type.

Parameters:
normalized_means (DataFrame): DataFrame containing the normalized means by school type.  """
    # Transformando os dados para o formato longo
    long_df = normalized_means.melt(id_vars=['TP_ESCOLA'], var_name='Área de Conhecimento', value_name='Média Normalizada')

    # Criando o gráfico
    plt.figure(figsize=(10, 6))
    for escola in long_df['TP_ESCOLA'].unique():
        escola_data = long_df[long_df['TP_ESCOLA'] == escola]
        plt.plot(escola_data['Área de Conhecimento'], escola_data['Média Normalizada'], label=escola)

    plt.title('Médias Normalizadas por Tipo de Escola e Área de Conhecimento', fontsize=14)
    plt.xlabel('Área de Conhecimento', fontsize=12)
    plt.ylabel('Média Normalizada', fontsize=12)
    plt.xticks(rotation=30, ha='right', fontsize=10)
    plt.legend(title='Tipo de Escola', fontsize=10)
    plt.tight_layout()
    plt.show()

def plot_normalized_boxplot(fortaleza_df):
    """
    Plots a boxplot of normalized grades by school type and area of ​​knowledge.

Parameters:
fortaleza_df (DataFrame): Filtered DataFrame containing data from Fortaleza.   """
    # Contando os alunos por tipo de escola
    counts = fortaleza_df['TP_ESCOLA'].value_counts()

    # Normalizando as notas pelo total de alunos por tipo de escola
    for col in ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']:
        fortaleza_df[col] = fortaleza_df[col] / fortaleza_df['TP_ESCOLA'].map(counts)

    # Transformando o DataFrame para o formato longo
    long_df = fortaleza_df.melt(
        id_vars=['TP_ESCOLA'],
        value_vars=['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO'],
        var_name='Área de Conhecimento',
        value_name='Nota Normalizada',
    )

    # Criando o boxplot
    area_renames = {
        'NU_NOTA_CN': 'Ciências da Natureza',
        'NU_NOTA_CH': 'Ciências Humanas',
        'NU_NOTA_LC': 'Linguagens e Códigos',
        'NU_NOTA_MT': 'Matemática',
        'NU_NOTA_REDACAO': 'Redação',
    }
    long_df['Área de Conhecimento'] = long_df['Área de Conhecimento'].replace(area_renames)

    plt.figure(figsize=(14, 8))
    sns.boxplot(data=long_df, x='Área de Conhecimento', y='Nota Normalizada', hue='TP_ESCOLA', palette='Set2')
    plt.title('Boxplot das Notas Normalizadas por Área de Conhecimento e Tipo de Escola', fontsize=16)
    plt.xlabel('Área de Conhecimento', fontsize=12)
    plt.ylabel('Nota Normalizada', fontsize=12)
    plt.xticks(rotation=30, ha='right')
    plt.legend(title='Tipo de Escola', fontsize=10, loc='upper right')
    plt.tight_layout()
    plt.show()

# Exemplo de uso
file_path = './MICRODADOS_ENEM_2023.csv'
fortaleza_df = get_student_counts(file_path)
normalized_means = calculate_normalized_means(fortaleza_df)
print(normalized_means)
plot_normalized_means(normalized_means)
plot_normalized_boxplot(fortaleza_df)
