import pandas as pd
import duckdb
import requests
from io import BytesIO
import warnings

# Suppress SSL warning
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# Download the Excel file (ignore SSL certificate validation)
url = "https://www.bcra.gob.ar/Pdfs/PublicacionesEstadisticas/historico-relevamiento-expectativas-mercado.xlsx"

def download_bcra_db():
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        excel_file = BytesIO(response.content)
        
        # Load the specific sheet, using the second row as header (row 2 in Excel is index 1)
        df = pd.read_excel(excel_file, sheet_name="Base de Datos Completa", header=1)
        
        # Optional cleanup: drop fully empty rows and unnamed columns
        df = df.dropna(how='all')  # Drop fully empty rows
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # Drop unnamed columns

        # Connect to DuckDB (or create one)
        con = duckdb.connect("bcra_macroeconomics.duckdb")
  
        con.execute("CREATE OR REPLACE TABLE raw_data AS SELECT * FROM df")
        con.close()

if __name__ == "__main__":
    download_bcra_db()