import pandas as pd

# Your dictionary, now with an additional column (Value 5)
data = {'x': [4, 5, 7, 2,0], 'y': [4,1, 10, 3, 8], 'z': [2,6, 9, 2, 4]}  # Added new values for Value 5

# Convert the dictionary into a DataFrame
df = pd.DataFrame.from_dict(data, orient='index', columns=['Value 1', 'Value 2', 'Value 3', 'Value 4', 'Value 5']).reset_index()
df.rename(columns={'index': 'Key'}, inplace=True)

# Normalize the values for each pair (1 & 2 -> blue, 3 & 4 -> red, 5 -> yellow)
normalized_blue = df[['Value 1', 'Value 2']].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
normalized_red = df[['Value 3', 'Value 4']].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
normalized_yellow = df[['Value 5']].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

# Normalize each column
df[['Value 1', 'Value 2']] = normalized_blue
df[['Value 3', 'Value 4']] = normalized_red
df[['Value 5']] = normalized_yellow

# Create a function to apply color formatting to the DataFrame
def apply_colors(val, col):
    if col == 'Value 1' or col == 'Value 2':
        return f'background-color: rgba(0, 0, 255, {val})'  # Blue gradient (higher value = more saturated)
    elif col == 'Value 3' or col == 'Value 4':
        return f'background-color: rgba(255, 0, 0, {val})'  # Red gradient (higher value = more saturated)
    elif col == 'Value 5':
        return f'background-color: rgba(255, 255, 0, {val})'  # Yellow gradient (higher value = more saturated)
    else:
        return ''

# Apply color formatting to the DataFrame using apply (not applymap)
styled_df = df.style.apply(lambda x: [apply_colors(v, col) for v, col in zip(x, x.index)], axis=1)

# Save the styled table as an HTML file using .to_html()
html_output = styled_df.to_html()

# Write to an HTML file
with open('styled_table.html', 'w') as f:
    f.write(html_output)

print("Table saved as 'styled_table.html'")

