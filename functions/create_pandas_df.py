import pandas as pd
from google.genai import types

dataframe_storage = {}

def create_df(csv_path: str, df_name: str, delimiter: str = ','):
    """
    Creates a DataFrame Pandas from a CSV file and saves it in memory with
    a specific name.
    """
    try:
        df = pd.read_csv(csv_path)
        dataframe_storage[df_name] = df
        return f"DataFrame '{df_name}' creato con successo da '{csv_path}'. Shape: {df.shape}"
    except Exception as e:
        f"Error creating dataframe: {e}"

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
            )
        },
        required=["csv_path", "df_name", "delimiter"]
    ),
)