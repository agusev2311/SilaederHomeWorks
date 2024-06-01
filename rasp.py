import os
import pandas as pd

# Define the URL of the Google Sheets document
url = "https://docs.google.com/spreadsheets/d/1DrPrx9IQcj_h2RnfekicMhYeU_rMXgVangiO_f9U5gc/edit#gid=1280018709"

# Define the file name for the output file
output_file = "rasp.tsv"

# Delete any existing file with the same name
if os.path.exists(output_file):
    os.remove(output_file)

# Read the first sheet of the Google Sheets document into a DataFrame
try:
    df = pd.read_csv(url, on_bad_lines='skip')
except pd.errors.ParserError as e:
    print("Error reading CSV file:", str(e))

# Save the DataFrame as a TSV file
df.to_csv(output_file, sep="\t", index=False)