import pandas as pd
import matplotlib.pyplot as plt

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
    selected_columns = ['NO_MUNICIPIO_PROVA', 'TP_ESCOLA']
    filtered_df = df[selected_columns]

    # Filtrando apenas os dados de Fortaleza
    fortaleza_df = filtered_df[filtered_df['NO_MUNICIPIO_PROVA'] == 'Fortaleza']

    # Mapeando os valores de TP_ESCOLA para maior legibilidade
    fortaleza_df['TP_ESCOLA'] = fortaleza_df['TP_ESCOLA'].replace({1: 'Não respondeu', 2: 'Pública', 3: 'Privada'})

    # Contagem de alunos por tipo de escola
    student_counts = fortaleza_df['TP_ESCOLA'].value_counts().to_dict()

    return student_counts

def plot_student_counts(student_counts):
    """
Plots a bar chart comparing total students by school type.

Parameters:
student_counts (dict): A dictionary of total students by school type.  """
    # Dados para o gráfico
    labels = list(student_counts.keys())
    counts = list(student_counts.values())

    # Criando o gráfico
    plt.figure(figsize=(8, 6))
    plt.bar(labels, counts, color=['skyblue', 'lightgreen', 'salmon'])
    plt.title('Total de Alunos por Tipo de Escola em Fortaleza', fontsize=14)
    plt.xlabel('Tipo de Escola', fontsize=12)
    plt.ylabel('Total de Alunos', fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.show()

# Exemplo de uso
file_path = './MICRODADOS_ENEM_2023.csv'
counts = get_student_counts(file_path)
plot_student_counts(counts)
