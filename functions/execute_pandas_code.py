import io
import contextlib
import sys
import os
import signal
from typing import Dict, Any
from google.genai import types
from .create_pandas_df import dataframes_storage
from .security import validate_path_within_working_directory
import pandas as pd

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException()

def execute_pandas_code(working_directory: str, code: str, timeout: int = 30):
    """
    Executes Python code with DataFrame access, timeout protection, and 
    strict working directory restrictions. All DataFrames are available as globals.
    """
    # Security: Validate working directory first
    try:
        safe_dir = validate_path_within_working_directory(working_directory)
    except ValueError as e:
        return f"Security error: {e}"
    
    # Security: Restrict builtins to prevent dangerous operations
    safe_builtins = {
        'print': print,
        'len': len, 'range': range, 'enumerate': enumerate,
        'str': str, 'int': int, 'float': float, 'bool': bool,
        'list': list, 'dict': dict, 'set': set, 'tuple': tuple,
        'isinstance': isinstance, 'type': type,
        'min': min, 'max': max, 'sum': sum, 'abs': abs,
        'round': round, 'zip': zip, 'sorted': sorted,
        # Add more safe builtins as needed
    }
    
    # Setup execution environment with DataFrames
    exec_globals: Dict[str, Any] = {
        'pd': pd,
        '__builtins__': safe_builtins,
        '__name__': '__main__',
    }
    exec_globals.update(dataframes_storage)  # Add all DataFrames
    
    # Capture stdout/stderr separately (like subprocess)
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    
    # Store original file descriptors
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    
    try:
        # Set working directory for any file I/O operations
        original_cwd = os.getcwd()
        os.chdir(safe_dir)
        
        # Set timeout (Unix/Linux/Mac only)
        if hasattr(signal, 'SIGALRM'):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout)
        
        # Redirect streams
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture
        
        # Execute code
        exec(code, exec_globals, {})
        
        # Cancel timeout
        if hasattr(signal, 'SIGALRM'):
            signal.alarm(0)
        
    except TimeoutException:
        return f"Error: Code execution timed out after {timeout} seconds"
    except Exception as e:
        # Cancel timeout
        if hasattr(signal, 'SIGALRM'):
            signal.alarm(0)
        return f"Error during execution: {type(e).__name__}: {e}\n" \
               f"STDERR:\n{stderr_capture.getvalue()}"
    finally:
        # Always restore original state
        os.chdir(original_cwd)
        sys.stdout = original_stdout
        sys.stderr = original_stderr
    
    # Format output like subprocess
    stdout_str = stdout_capture.getvalue()
    stderr_str = stderr_capture.getvalue()
    
    output_parts = []
    if stdout_str:
        output_parts.append(f"STDOUT:\n{stdout_str}")
    if stderr_str:
        output_parts.append(f"STDERR:\n{stderr_str}")
    
    if not output_parts:
        return "Code executed successfully, no output produced."
    
    return "\n".join(output_parts)

# Updated schema
schema_execute_pandas_code = types.FunctionDeclaration(
    name="execute_pandas_code",
    description="Executes Python/Pandas code with DataFrame access, timeout protection, and working directory restriction. All loaded DataFrames are available as global variables.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="Working directory path for code execution (relative to configured WORKING_DIR)."
            ),
            "code": types.Schema(
                type=types.Type.STRING,
                description="Python code string to execute. Use print() to display results."
            ),
            "timeout": types.Schema(
                type=types.Type.INTEGER,
                description="Optional timeout in seconds (default 30, max 300)."
            )
        },
        required=["working_directory", "code"]
    )
)