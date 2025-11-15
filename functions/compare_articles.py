# file: functions/compare_articles.py

import pandas as pd
from google.genai import types

# Importiamo il dizionario dove sono salvati i DataFrame
from .create_pandas_df import dataframes_storage

def compare_articles(source_df_name: str, pimcore_df_name: str, article_code: str):
    """
    Finds a specific article by its code in both source and pimcore dataframes,
    performs cleaning, and returns a detailed comparison.
    """
    try:
        # Recupera i DataFrame dalla memoria
        if source_df_name not in dataframes_storage or pimcore_df_name not in dataframes_storage:
            return "Error: One or both DataFrames are not loaded in memory."
        
        df_source = dataframes_storage[source_df_name]
        df_pimcore = dataframes_storage[pimcore_df_name]

        # --- Logica di pulizia e confronto robusta (scritta da noi) ---
        
        # Pulisci le colonne chiave in entrambi i df
        source_key_cleaned = df_source['Articolo'].astype(str).str.strip().str.upper()
        pimcore_key_cleaned = df_pimcore['dcTitle'].astype(str).str.strip().str.upper()
        
        # Pulisci il codice articolo in input per sicurezza
        clean_article_code = str(article_code).strip().upper()

        # Cerca il record
        source_record = df_source[source_key_cleaned == clean_article_code]
        pimcore_record = df_pimcore[pimcore_key_cleaned == clean_article_code]

        if source_record.empty:
            return f"Article '{clean_article_code}' not found in the source DataFrame."
        if pimcore_record.empty:
            return f"Article '{clean_article_code}' FOUND in source but NOT FOUND in Pimcore DataFrame."

        # Estrai la prima riga trovata
        source_row = source_record.iloc[0]
        pimcore_row = pimcore_record.iloc[0]

        # Mappatura delle colonne
        mapping = {
            'Articolo': 'dcTitle',
            'Descrizione Ital.': 'dcDescription',
            'Stag.applicazione': 'stagione_applicazione',
            'Provenienza mat.': 'prov_mat',
            'Cod. composizione': 'cod_comp',
            'Peso Finito 1': 'peso_fin_1',
            'Peso Finito 2': 'peso_fin_2',
            'Commento  1': 'commento_1',
            'Peso Finito Prod.': 'peso_fin_prod',
            'Peso Metro Quadro':  'peso_metro_quadro',
            'Peso Greggio': 'peso_greggio',
            'Alt.za Finita': 'alt_finita',
            'Commento  1': 'commento_1',
            'Commento  2': 'commento_2'

        }

        # Costruisci una stringa di report chiara
        report = [f"--- Comparison Report for Article: {clean_article_code} ---"]
        for source_col, pimcore_col in mapping.items():
            source_val = source_row.get(source_col, 'N/A')
            pimcore_val = pimcore_row.get(pimcore_col, 'N/A')
            report.append(f"\n- {source_col} / {pimcore_col}:")
            report.append(f"  - Source:  {source_val}")
            report.append(f"  - Pimcore: {pimcore_val}")
        
        return "\n".join(report)

    except Exception as e:
        return f"An unexpected error occurred during comparison: {e}"

schema_compare_articles = types.FunctionDeclaration(
    name="compare_articles",
    description="Compares a single record between the source and pimcore dataframes using a specific article code.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "source_df_name": types.Schema(type=types.Type.STRING, description="The name of the source DataFrame (e.g., 'df_source')."),
            "pimcore_df_name": types.Schema(type=types.Type.STRING, description="The name of the pimcore DataFrame (e.g., 'df_pimcore')."),
            "article_code": types.Schema(type=types.Type.STRING, description="The article code to search for and compare."),
        },
        required=["source_df_name", "pimcore_df_name", "article_code"]
    )
)