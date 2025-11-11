import pandas as pd

def create_df(csv_path):
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        f"Error creating dataframe: {e}"

