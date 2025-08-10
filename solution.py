import pandas as pd
import re
from pandas.api.types import is_numeric_dtype

def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    """Adds a virtual column to the DataFrame based on the provided role expression."""
    valid_name_re = re.compile(r"^[A-Za-z_]+$")
    if not isinstance(df, pd.DataFrame) or df.empty:
        return pd.DataFrame()
    if not isinstance(new_column, str) or not valid_name_re.match(new_column):
        return pd.DataFrame()
    if not all(isinstance(c, str) and valid_name_re.match(c) for c in df.columns):
        return pd.DataFrame()
    if not isinstance(role, str):
        return pd.DataFrame()

    expr = role.strip()
    if not re.fullmatch(r"[A-Za-z_+\-* \t]+", expr):
        return pd.DataFrame()

    expr_columns = re.findall(r"[A-Za-z_]+", expr)
    if not all(col in df.columns for col in expr_columns):
        return pd.DataFrame()
    if not all(is_numeric_dtype(df[col]) for col in expr_columns):
        return pd.DataFrame()

    try:
        result_series = pd.eval(expr, engine='python', parser='pandas', local_dict=df.to_dict('series'))
        result_df = df.copy()
        result_df[new_column] = result_series
        return result_df
    except Exception:
        return pd.DataFrame()
