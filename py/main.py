import pandas as pd
import random

from function import *

EXCEL_PATH = "medicine.xlsx"
MODIFY_COL_DRUG = ['type', 'other bac', 'group', 'no']
MODIFY_COL_BAC = ['type shape']

drugs = pd.read_excel(EXCEL_PATH, sheet_name='Sheet4', index_col=0)
bacs = pd.read_excel(EXCEL_PATH, sheet_name='Sheet22', index_col=0)
drugs, bacs = modify_drugs(MODIFY_COL_DRUG, MODIFY_COL_BAC, drugs, bacs)	
#create_question(bacs, drugs)

bacs['type shape'].to_json('bacs.json',orient="columns", indent=4)

drugs.set_index('drug')['bac'].to_json('drugs.json',orient="columns", indent=4)
