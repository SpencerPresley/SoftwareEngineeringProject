import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('commit_details.csv')

# Filter the DataFrame for entries related to Jude
jude_df = df[df['author'].str.contains("Jude")]

# Group by filePath, additions, and deletions to find duplicates or similar changes
grouped_jude = jude_df.groupby(['filePath', 'additions', 'deletions']).size().reset_index(name='counts')

# Filter to show only entries with more than one occurrence
duplicates_jude = grouped_jude[grouped_jude['counts'] > 1]

# Sort by filePath and counts to better visualize the duplicates
duplicates_jude = duplicates_jude.sort_values(by=['filePath', 'counts'], ascending=False)

# Print the result
print(duplicates_jude)