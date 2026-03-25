import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

class LeadDataProcessor:
    """
    Handles data cleaning, missing value imputation, and feature scaling
    for the LeadFlow-ML pipeline.
    """
    def __init__(self):
        self.imputer = SimpleImputer(strategy='median')
        self.scaler = StandardScaler()

    def clean_data(self, df):
        # Fill missing values for numerical columns
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        df[numeric_cols] = self.imputer.fit_transform(df[numeric_cols])

        # Outlier capping for web engagement metrics
        if 'time_on_site_sec' in df.columns:
            upper_limit = df['time_on_site_sec'].quantile(0.99)
            df['time_on_site_sec'] = df['time_on_site_sec'].clip(upper=upper_limit)

        return df

    def scale_features(self, X_train, X_test):
        # Standardizing features to have mean=0 and variance=1
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        return X_train_scaled, X_test_scaled
