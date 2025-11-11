from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.create_pandas_df import schema_create_df

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_create_df,
    ]
)