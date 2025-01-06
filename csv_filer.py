#Code used to filter csv columns

import pandas as pd

file_path = r'D:/University/PEST/file.csv' #path to csv file
df = pd.read_csv(file_path, encoding='latin-1', sep=';')

aggregated_df = df.groupby(['NO_MUNICIPIO_PROVA', 'TP_ESCOLA', 'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']).size().reset_index()


output_file_path = r'D:/University/PEST/ENEM-2023-DATA-ANALYSIS/MICRODADOS_ENEM_2023.csv' # creates a new csv file with the selected columns

aggregated_df.to_csv(output_file_path, index=False)

