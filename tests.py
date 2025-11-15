# file: debug_pandas.py

import pandas as pd

# --- Impostazioni ---
# Definiamo i percorsi e il codice che stiamo cercando
PIMCORE_FILE_PATH = 'data/tg_export_Articoli_Pimcore.csv'
ARTICLE_CODE_TO_FIND = '80G21' # Il codice che continua a fallire

print(f"--- Inizio Debug: Ricerca dell'articolo '{ARTICLE_CODE_TO_FIND}' ---")

try:
    # --- Passo 1: Carica il file CSV di Pimcore con le opzioni più robuste ---
    # Usiamo le stesse opzioni dell'agente, ma aggiungiamo low_memory=False
    # low_memory=False forza Pandas a leggere tutto il file subito, migliorando
    # l'affidabilità del tipo di dato.
    print(f"\n[1] Caricamento del file: {PIMCORE_FILE_PATH}")
    df_pimcore = pd.read_csv(
        PIMCORE_FILE_PATH,
        delimiter=';',
        encoding='latin-1',
        dtype=str,          # Forza tutto a stringa
        low_memory=False    # Aumenta l'affidabilità del caricamento
    )
    print(f"    -> Caricamento completato. Shape del DataFrame: {df_pimcore.shape}")

    # --- Passo 2: Applica la pulizia alla colonna dcTitle ---
    print("\n[2] Pulizia della colonna 'dcTitle'...")
    df_pimcore['cleaned_title'] = df_pimcore['dcTitle'].str.strip().str.upper()
    print("    -> Colonna 'cleaned_title' creata.")

    # --- Passo 3: Pulisci il codice che stiamo cercando ---
    clean_code_to_find = ARTICLE_CODE_TO_FIND.strip().upper()
    print(f"\n[3] Codice pulito da cercare: '{clean_code_to_find}'")

    # --- Passo 4: Esegui la ricerca ---
    print("\n[4] Esecuzione della ricerca booleana...")
    matches = df_pimcore['cleaned_title'] == clean_code_to_find
    
    # --- Passo 5: Analizza i risultati ---
    print("\n--- RISULTATI ---")
    num_matches = matches.sum() # True conta come 1, False come 0
    print(f"Numero di corrispondenze trovate: {num_matches}")

    if num_matches > 0:
        print("\nARTICOLO TROVATO! Ecco il record corrispondente:")
        # Mostra la riga o le righe che hanno corrisposto
        print(df_pimcore[matches][['dcTitle', 'cleaned_title', 'dcDescription']])
    else:
        print("\nARTICOLO NON TROVATO. Qualcosa non quadra.")
        # Proviamo a vedere se troviamo qualcosa di simile
        partial_matches = df_pimcore[df_pimcore['cleaned_title'].str.contains(clean_code_to_find, na=False)]
        if not partial_matches.empty:
            print("\nPerò, ho trovato queste corrispondenze parziali che potrebbero essere utili:")
            print(partial_matches[['dcTitle', 'cleaned_title', 'dcDescription']])
        else:
            print("Nessuna corrispondenza, nemmeno parziale, è stata trovata.")
            print(df_pimcore.head())

except Exception as e:
    print(f"\nERRORE DURANTE L'ESECUZIONE DELLO SCRIPT: {e}")