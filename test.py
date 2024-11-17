import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from function import *

EXCEL_PATH = "medicine.xlsx"
MODIFY_COL_DRUG = ['type', 'other bac', 'group', 'no']
MODIFY_COL_BAC = ['type shape']

drugs = pd.read_excel(EXCEL_PATH, sheet_name='Sheet4', index_col=0)
bacs = pd.read_excel(EXCEL_PATH, sheet_name='Sheet22', index_col=0)
drugs, bacs = modify_drugs(MODIFY_COL_DRUG, MODIFY_COL_BAC, drugs, bacs)	
drug_bac = dict()
for index,row in drugs.iterrows():
	pb = 0
	pc = 0
	nb = 0
	nc = 0
	m = 0
	other = []
	for bac in row['bac']:
		t = bacs.loc[bac]['type shape']
		if t == 'positive bacilli':
			pb += 1
		elif t == 'positive strep' or t == 'positive staph':
			pc += 1
		elif t == 'negative bacilli' or t == 'negative spiral':
			nb += 1
		elif t == 'negative coccobacilli' or t == 'negative diplococci':
			nc += 1
		elif t == 'mycobacterium':
			m += 1
		else:
			other.append(t)

	drug_bac[row['drug']] = [pb, pc, nb, nc, m]

# Convert the dictionary into a DataFrame
df = pd.DataFrame.from_dict(drug_bac, orient='index', columns=['Positive bacilli', 'Positive cocci', 'Negative bacilli', 'Negative cocci', 'Mycobacterium']).reset_index()
df.rename(columns={'index': 'Drug name'}, inplace=True)

# Normalize the values for each pair (1 & 2 -> blue, 3 & 4 -> red)
normalized_blue = df[['Positive bacilli', 'Positive cocci']].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
normalized_red = df[['Negative bacilli', 'Negative cocci']].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
normalized_yellow = df[['Mycobacterium']].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

# Create a figure and axis
fig, ax = plt.subplots(figsize=(6, 3))

# Hide axes
ax.axis('tight')
ax.axis('off')

# Create color maps
cmap_blue = sns.light_palette("blue", as_cmap=True)
cmap_red = sns.light_palette("red", as_cmap=True)
cmap_yellow = sns.light_palette("yellow", as_cmap=True)

# Define a cell format (empty cells for values)
table_values = []
for i, row in df.iterrows():
    table_values.append([row['Drug name'], '', '', '', '', ''])  # Leave values empty

# Create a table
table = ax.table(
    cellText=table_values,
    colLabels=['Drug name', 'Positive bacilli', 'Positive cocci', 'Negative bacilli', 'Negative cocci', 'Mycobacterium'],
    cellLoc='center',
    loc='center',
    colWidths=[0.15, 0.15, 0.15, 0.15, 0.15, 0.15]
)

# Style the table
header_color = "#D3D3D3"  # Light gray background for the header
header_fontweight = "bold"  # Bold font for the header
for (row, col), cell in table.get_celld().items():
    if row == 0:  # Header row
        cell.set_facecolor(header_color)
        cell.set_text_props(weight=header_fontweight)
    if col == 0 and row > 0:  # Bold text for the first column (Keys)
        cell.set_text_props(weight="bold")
    if row > 0:  # Style the data rows
        if 1 <= col <= 2:  # Value 1 and Value 2 (blue)
            value = float(df.iloc[row - 1, col])
            color = cmap_blue(value / df[['Positive bacilli', 'Positive cocci']].values.max())
            cell.set_facecolor(color)
        if 3 <= col <= 4:  # Value 3 and Value 4 (red)
            value = float(df.iloc[row - 1, col])
            color = cmap_red(value / df[['Negative bacilli', 'Negative cocci']].values.max())
            cell.set_facecolor(color)
        if col == 5:  # Value 3 and Value 4 (red)
            value = float(df.iloc[row - 1, col])
            color = cmap_yellow(value / df[['Mycobacterium']].values.max())
            cell.set_facecolor(color)
    cell.set_linewidth(0.5)
    cell.set_fontsize(8)
# Adjust layout and display
plt.show()

