import pandas as pd


class AnalysisService:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def summary(self) -> pd.DataFrame:
        summary_df = pd.DataFrame(
            {
                "Column": self.df.columns,
                "# Rows": [self.df.shape[0] for _ in self.df.columns],
                "# Nulls": [self.df[col].isna().sum() for col in self.df.columns],
                "Type": [self.df[col].dtype for col in self.df.columns],
            }
        )

        duplicated_rows = self.df.duplicated().sum()

        print(summary_df)
        print(f"\n{duplicated_rows} duplicated rows")

        return summary_df

    @staticmethod
    def related_columns(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        common_columns = set(df1.columns) & set(df2.columns)
        validation = []

        for col in common_columns:
            only_in_df1 = set(df1[col].dropna()) - set(df2[col].dropna())
            only_in_df2 = set(df2[col].dropna()) - set(df1[col].dropna())

            validation.append(
                {
                    "column": col,
                    "df1_nulls": df1[col].isna().sum(),
                    "df2_nulls": df2[col].isna().sum(),
                    "only_df1": len(only_in_df1),
                    "only_df2": len(only_in_df2),
                }
            )

        val_df = pd.DataFrame(validation)

        print(f"\nCommon columns: {common_columns}\n")
        print(val_df)

        return val_df
