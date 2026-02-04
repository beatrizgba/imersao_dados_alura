import pandas as pd
import pycountry

# abrir o arquivo
dataframe = pd.read_csv("https://raw.githubusercontent.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv")

# entender o conteudo
# print(dataframe.head())   
# print(dataframe.info())
# print(dataframe.columns)
# print(dataframe.describe())
# print(dataframe.shape)
# print(dataframe.isnull().sum()) 
# print(dataframe['ano'].unique())

# renomear colunas
renomear_colunas = {
    'work_year': 'ano',
    'experience_level': 'senioridade',
    'employment_type': 'contrato',
    'job_title': 'cargo',
    'salary': 'salario',
    'salary_currency': 'moeda',
    'salary_in_usd': 'usd',
    'employee_residence': 'residencia',
    'remote_ratio': 'remoto',
    'company_location': 'empresa',
    'company_size': 'tamanho_empresa'
}

dataframe.rename(columns=renomear_colunas, inplace=True)
# Inplace = no arquivo em si, o original

# Ajustar valores de colunas
# senioridade
substituir_senioridade = {
    "SE": "Senior",
    "MI": 'Pleno',
    "EN": 'Junior',
    "EX": "Executivo"
}

# dataframe["senioridade"] = dataframe['senioridade'].map(substituir_senioridade) ou:
dataframe["senioridade"] = dataframe['senioridade'].replace(substituir_senioridade)

# contrato
substituir_contrato = {
    "FT": "Tempo Integral",
    "PT": 'Tempo Parcial',
    "CT": "Freela"
}

dataframe['contrato'] = dataframe['contrato'].replace(substituir_contrato)

substituir_remoto = {
    0: "Presencial",
    100: 'Remoto',
    50: 'Híbrido'
}

# remoto
dataframe["remoto"] = dataframe["remoto"].replace(substituir_remoto)

# tamanho da empresa
substituir_tamanho_empresa = {
    "M": "Média",
    "L": 'Grande',
    "S": 'Pequena'
}

dataframe['tamanho_empresa'] = dataframe["tamanho_empresa"].replace(substituir_tamanho_empresa)

# apenas alguns linhas tem nulo, então podemos remover essas linhas
df_limpo = dataframe.dropna()

# ano esta como float, vamos converter para int
df_limpo = df_limpo.assign(ano=df_limpo['ano'].astype('int64'))

# converter pais de 2 digitos para 3 dígitos (ISO2 para ISO3)
def is2_to_iso3code(code):
  try:
    return pycountry.countries.get(alpha_2=code).alpha_3
  except:
    return None

# criar nova coluna com o código ISO3
df_limpo['residencia_iso3'] = df_limpo['residencia'].apply(is2_to_iso3code)

# salvar o arquivo limpo
df_limpo.to_csv("dados_imersao_alura_limpo.csv", index=False)

