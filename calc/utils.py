# utils.py
import pandas as pd
from .models import KPI , Employee  # Import your Django model

def process_excel_file(excel_file):
    # Read Excel file using pandas or your preferred library
    df = pd.read_excel(excel_file)

    # Process the data as needed
    # ...

    # Example: Create instances of a Django model
    # for index, row in df.iterrows():
    #     YourModel.objects.create(field1=row['column1'], field2=row['column2'], ...)  # Adjust fields accordingly
