import pandas as pd
from sklearn.impute import KNNImputer

def detect_missing_data(df):
    missing_data = df.isnull().sum()
    missing_data_percentage = (missing_data / len(df)) * 100
    missing_report = pd.DataFrame({'Missing Values': missing_data, 'Percentage': missing_data_percentage})
    missing_report = missing_report[missing_report['Missing Values'] > 0]
    print("Missing Data Report:\n", missing_report)
    return missing_report

def impute_missing_values(df):
    for col in df.select_dtypes(include=['float64', 'int64']).columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)

    for col in df.select_dtypes(include=['object']).columns:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)

    return df

def advanced_imputation(df, n_neighbors=5):
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
    imputer = KNNImputer(n_neighbors=n_neighbors)
    df[numerical_cols] = imputer.fit_transform(df[numerical_cols])
    return df

# Eg
mapped_data_file = "path/to/your/usagi_mappings.csv"
df = pd.read_csv(mapped_data_file)

missing_report = detect_missing_data(df)
df_imputed = impute_missing_values(df)
df_advanced_imputed = advanced_imputation(df_imputed)

df_advanced_imputed.to_csv("path/to/your/imputed_data.csv", index=False)
print("Saved to imputed_data.csv")
