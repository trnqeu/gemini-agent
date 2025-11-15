import pandas as pd
from google.genai import types

dataframes_storage = {}

def create_df(csv_path: str, df_name: str, delimiter: str = ',', encoding: str = 'utf-8', dtype=str):
    """
    Creates a DataFrame Pandas from a CSV file and saves it in memory with
    a specific name.
    """
    try:
        df = pd.read_csv(csv_path, delimiter = delimiter, encoding = encoding, low_memory=False, index_col=False)
        dataframes_storage[df_name] = df
        return f"DataFrame '{df_name}' creato con successo da '{csv_path}'. Shape: {df.shape}"
    except Exception as e:
        return f"Error creating dataframe: {e}"

schema_create_df = types.FunctionDeclaration(
    name="create_df",
    description="Creates a DataFrame Pandas from a CSV file and saves it in memory with a specific name.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "csv_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the csv file.",
            ),
            "df_name": types.Schema(
                type=types.Type.STRING,
                description="the name of the dataframe"
            ),
            "delimiter": types.Schema(
                type=types.Type.STRING,
                description="The delimiter that separates the csv file's columns (e.g. ',', ';')"
            ),
            "encoding": types.Schema(
                type=types.Type.STRING,
                description="The encoding of the file. Defaults to 'utf-8'. Use 'latin-1' or 'cp1252' for common legacy files."
            )
        },
        required=["csv_path", "df_name", "delimiter"]
    ),
)