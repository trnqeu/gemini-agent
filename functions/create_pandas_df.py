import pandas as pd
from google.genai import types


def create_df(csv_path):
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        f"Error creating dataframe: {e}"



schema_create_df = types.FunctionsDeclaration(
    name="create_df",
    description="Creates a Pandas dataframe from a csv file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "csv_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the csv file.",
            ),
        },
    ),
)