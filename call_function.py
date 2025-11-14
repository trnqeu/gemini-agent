from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.create_pandas_df import create_df, schema_create_df
from functions.execute_pandas_code import execute_pandas_code, schema_execute_pandas_code

from config import WORKING_DIR


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_create_df,
        schema_execute_pandas_code
    ]
)

def call_function(function_call_part, verbose=False):
    function_map = {
        "get_files_info": get_files_info,
        "create_df": create_df,
        "execute_pandas_code": execute_pandas_code
    }
    
    function_name = function_call_part.name
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"}
            )]
        )
    
    args = dict(function_call_part.args)
    
    # Only add working_directory for functions that need it
    if function_name in ["get_files_info", "execute_pandas_code"]:
        args["working_directory"] = WORKING_DIR
    
    function_result = function_map[function_name](**args)
    
    return types.Content(
        role="tool",
        parts=[types.Part.from_function_response(
            name=function_name,
            response={"result": function_result}
        )]
    )