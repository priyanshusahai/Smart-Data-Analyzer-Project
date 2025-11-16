import pandas as pd
from ydata_profiling import ProfileReport

class DataProfiler:
    """Handles data profiling and summary generation."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    # 1. BASIC SUMMARY
    def get_basic_summary(self):
        return {
            "num_rows": self.df.shape[0],
            "num_columns": self.df.shape[1],
            "columns": list(self.df.columns)
        }

    # 2. MISSING VALUES
    def get_missing_summary(self):
        missing = self.df.isna().sum()
        percent = (missing / len(self.df)) * 100

        summary = pd.DataFrame({
            "missing_count": missing,
            "missing_percent": percent.round(2)
        })

        return summary.sort_values("missing_percent", ascending=False)

    # 3. NUMERIC SUMMARY
    def get_numeric_summary(self):
        return self.df.describe(include="number").T

    # 4. CATEGORICAL SUMMARY
    def get_categorical_summary(self):
        cat_df = self.df.select_dtypes(include="object")
        return cat_df.nunique().sort_values(ascending=False)

    # 5. DUPLICATE SUMMARY
    def get_duplicate_summary(self):
        duplicate_count = self.df.duplicated().sum()
        return {
            "duplicate_rows": duplicate_count,
            "duplicate_percent": round(duplicate_count / len(self.df) * 100, 2)
        }

    # 6. --- FIX ADDED HERE ---
    def get_profile_report(self, output_file="static/report.html"):
        """Generate and save the profiling HTML report."""
        profile = ProfileReport(self.df, title="Smart Data Profiler Report")
        profile.to_file(output_file)
        return output_file
