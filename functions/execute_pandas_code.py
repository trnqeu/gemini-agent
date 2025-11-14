import io
import contextlib
from google.genai import types

# import dictionary with dataframes names
from .create_pandas_df import dataframes_storage
import pandas as pd


def execute_pandas_code(code: str):
    """
    Executes a string of python code that operates 
    on the Dataframes saved in memory.
    """
    # uses buffer to capture the output of the executed code
    output_buffer = io.StringIO()

    try:
        # redirects the standard output to the buffer
        with contextlib.redirect_stdout(output_buffer):
            """
            Execute the code. Pass dataframes dictionary
            as a union of global and local variables.
            """
            exec(code, {'pd': pd, **dataframes_storage}, dataframes_storage)

        result = output_buffer.getvalue()
        if not result:
            return "Code executed, no output produced."
        return f"Output del codice:\n---\n{result}\n---"
        
    except Exception as e:
        return f"Errore durante l'esecuzione del codice: {e}"
    
schema_execute_pandas_code = types.FunctionDeclaration(
    name="execute_pandas_code",
    description = "Runs Python code using the Pandas library on previously loaded DataFrames. DataFrames are available as global variables with the name provided during their creation.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "code": types.Schema(
                type=types.Type.STRING,
                description="A string containing Python code to run."
            ),
        },
        required=["code"]
        ),
    )
