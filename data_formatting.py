import pandas as pd
import re
from datetime import datetime

def enforce_data_types(df, schema):
    for column, dtype in schema.items():
        if column in df.columns:
            try:
                df[column] = df[column].astype(dtype)
            except ValueError:
                print(f"Warning: Could not convert column {column} to {dtype}.")
    return df

def standardize_dates(df, date_columns):
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d')
    return df

def clean_strings(df, string_columns):
    for col in string_columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: re.sub(r'[^a-zA-Z0-9 ]', '', str(x)) if pd.notnull(x) else x)
    return df

# Eg
omop_schema = {
    'person_id': 'int64',
    'gender_concept_id': 'int64',
    'birth_datetime': 'datetime64[ns]',
    'visit_date': 'datetime64[ns]',
    'condition_concept_id': 'int64',
    'drug_concept_id': 'int64',
    'quantity': 'float64',
    'cost': 'float64'
}

date_columns = ['birth_datetime', 'visit_date']
string_columns = ['condition_source_value', 'drug_source_value']
imputed_data_file = "path/to/your/imputed_data.csv"
df = pd.read_csv(imputed_data_file)

df = enforce_data_types(df, omop_schema)
df = standardize_dates(df, date_columns)
df = clean_strings(df, string_columns)

df.to_csv("path/to/your/standardized_data.csv", index=False)