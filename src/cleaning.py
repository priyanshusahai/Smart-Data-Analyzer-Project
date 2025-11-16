import pandas as pd
import numpy as np


class DataCleaner:
    """Handles cleaning operations + auto suggestions."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    # -----------------------------------------------------------------------
    # 1. SUGGEST CLEANING ACTIONS (industry-style suggestions)
    # -----------------------------------------------------------------------
    def suggest_actions(self):
        suggestions = []

        # Missing values
        missing_percent = (self.df.isna().sum() / len(self.df)) * 100
        for col, percent in missing_percent.items():
            if percent == 0:
                continue
            elif percent > 50:
                suggestions.append(
                    f"Column '{col}' has {percent:.1f}% missing values → Consider DROPPING this column."
                )
            elif percent > 20:
                suggestions.append(
                    f"Column '{col}' has {percent:.1f}% missing → Consider imputing with MEDIAN/ MODE."
                )
            else:
                suggestions.append(
                    f"Column '{col}' has {percent:.1f}% missing → Safe to FILL with mean/median/mode."
                )

        # Duplicates
        dup_count = self.df.duplicated().sum()
        if dup_count > 0:
            suggestions.append(
                f"Dataset contains {dup_count} duplicate rows → You should DROP duplicates."
            )

        # Outliers (basic IQR logic on numeric columns)
        numeric_cols = self.df.select_dtypes(include=np.number).columns
        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            outlier_count = ((self.df[col] < lower) | (self.df[col] > upper)).sum()

            if outlier_count > 5:
                suggestions.append(
                    f"Column '{col}' has {outlier_count} potential outliers → Consider treating them."
                )

        return suggestions

    # -----------------------------------------------------------------------
    # 2. DROP ROWS WITH NULLS
    # -----------------------------------------------------------------------
    def drop_rows_with_missing(self, columns=None):
        """Drops rows containing NaN in specific columns or all columns."""
        if columns:
            self.df = self.df.dropna(subset=columns)
        else:
            self.df = self.df.dropna()
        return self.df

    # -----------------------------------------------------------------------
    # 3. DROP COLUMNS WITH HIGH MISSING VALUES
    # -----------------------------------------------------------------------
    def drop_columns_with_missing(self, threshold=50):
        """Drops columns where missing % exceeds threshold."""
        missing_percent = (self.df.isna().sum() / len(self.df)) * 100
        cols_to_drop = missing_percent[missing_percent > threshold].index
        self.df = self.df.drop(columns=cols_to_drop)
        return self.df, list(cols_to_drop)

    # -----------------------------------------------------------------------
    # 4. FILL MISSING VALUES
    # -----------------------------------------------------------------------
    def fill_missing(self, strategy="mean", columns=None):
        """Fill missing values based on strategy."""
        df = self.df

        if columns is None:
            columns = df.columns

        for col in columns:
            if df[col].dtype in ["int64", "float64"]:
                if strategy == "mean":
                    df[col] = df[col].fillna(df[col].mean())
                elif strategy == "median":
                    df[col] = df[col].fillna(df[col].median())
                elif strategy == "zero":
                    df[col] = df[col].fillna(0)

            else:  # categorical
                df[col] = df[col].fillna(df[col].mode()[0])

        self.df = df
        return self.df

    # -----------------------------------------------------------------------
    # 5. REMOVE DUPLICATES
    # -----------------------------------------------------------------------
    def remove_duplicates(self):
        """Drops duplicate rows."""
        before = len(self.df)
        self.df = self.df.drop_duplicates()
        after = len(self.df)
        return self.df, before - after

    # -----------------------------------------------------------------------
    # 6. OUTLIER TREATMENT (IQR Capping)
    # -----------------------------------------------------------------------
    def treat_outliers(self, columns=None):
        """Caps outliers using IQR method."""
        df = self.df

        if columns is None:
            columns = df.select_dtypes(include=np.number).columns

        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            df[col] = np.where(df[col] < lower, lower,
                               np.where(df[col] > upper, upper, df[col]))

        self.df = df
        return self.df

    # -----------------------------------------------------------------------
    # 7. RETURN CLEANED DATA
    # -----------------------------------------------------------------------
    def get_cleaned_data(self):
        return self.df
