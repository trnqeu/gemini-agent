# Risultati 

## Prompt

```
uv run main.py "Ciao, ho due file CSV all'interno della cartella data: uno è delimitato da virgola, uno da punto e virgola. Voglio che tu scelga un articolo a caso dal primo file, lo cerchi nel secondo file confrontando la colonna 'Articolo' con 'dcTitle', e verifichi che i dati siano stati importati correttamente usando la funzione executes_pandas_call. Mostrami un confronto." --verbose
```

```

uv run main.py "Ciao, ho due file CSV all'interno della cartella data: uno è delimitato da virgola, uno da punto e virgola. Voglio che tu scelga un articolo a caso dal primo file, lo cerchi nel secondo file confrontando la colonna 'Articolo' con 'dcTitle', e verifichi che i dati siano stati importati correttamente usando la funzione executes_pandas_call. I valori all'interno della colonna Articolo potrebbero avere degli spazi all'inizio o alla fine, per cui andrebbero trimmati al fine di poter fare un confronto con i valori dell'atro file, che sono invece già trimmati.  Mostrami un confronto tra i due articoli. I file si chiamano data/tf_vdibart.csv e data/tg_export_Articoli_Pimcore.csv" --verbose
```

Dopo il potenziamento del system_prompt:

```
uv run main.py "Avvia il processo di verifica dei dati tra il file sorgente e quello di Pimcore. Seleziona un articolo casuale e mostrami il confronto dettagliato come da istruzioni." --verbose
```

## No match
L'agente non è riuscito a trovare l'articolo corrispondente perché i dati dentro la colonna Articolo non sono trimmati.

**Soluzione** -> miglioramento del prompt

## Codifica
L'agente riscontra un problema di codifica del file csv: dice che il csv non è utf-8

**Soluzione** -> aggiungere il parametro encoding alla funzione create_pandas_df

## Non capisce cosa fare
L'agente non capisce che tipo di confronto deve fare

**Soluzione**-> Potenziamento del system prompt con una mappatura campo per campo

## Non trova l'articolo corrispondente

**Soluzione**-> potenziamento del sistem prompt, creando una sequenza di comandi obbligatoria.

 Generate and execute **a single Python script** using the `execute_pandas_code` tool. This script must:
    a. Create new, cleaned key columns in both DataFrames. For example:
       `df_source['cleaned_articolo'] = df_source['Articolo'].astype(str).str.strip().str.upper()`
       `df_pimcore['cleaned_dctitle'] = df_pimcore['dcTitle'].astype(str).str.strip().str.upper()`


Cosa ha davvero funzionato:

```
low_memory=False,
index_col=False
```