import pandas as pd
from fancyimpute import KNN, SoftImpute

dataset = pd.read_csv('cut_dataset_merged.csv')

# Искючение колон с типом данных string (т.к. STOCHASTIC REGRESSION IMPUTATION иначе выдаст ошибку)
excluded_columns = ['mol_id','smiles', 'iupac_name', 'atom_stereo_count']
strings_dataset = dataset[excluded_columns]

# Получение нового DataFrame только с указанными столбцами
included_columns = [col for col in dataset.columns if col not in excluded_columns]
excluded_dataset = dataset[included_columns]

soft_impute = SoftImpute()
df_imputed = pd.DataFrame(soft_impute.fit_transform(excluded_dataset), columns=excluded_dataset.columns)

# Получение нормализованных данных
normalized_data = strings_dataset.join(df_imputed)

normalized_data.to_csv('normalized_data.csv', index=False)