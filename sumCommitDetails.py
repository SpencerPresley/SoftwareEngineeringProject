import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('commit_details.csv')

# Ensure the data types are integers for numerical operations
df['additions'] = pd.to_numeric(df['additions'], errors='coerce')
df['deletions'] = pd.to_numeric(df['deletions'], errors='coerce')
df['filesChanged'] = pd.to_numeric(df['filesChanged'], errors='coerce')

# Calculate total and net changes
df['totalChanges'] = df['additions'] + df['deletions']
df['netChanges'] = df['additions'] - df['deletions']

# Define a mapping of aliases to a canonical author name
author_aliases = {
    'SpencerPresley': 'Spencer Presley',
    'cbarbes1': 'Cole Barbes',
    'cbarbes': 'Cole Barbes',
    'Jude': 'Jude Maggitti',
    'Underlord711': 'Will Chmar',
}

# Map the author names using the aliases dictionary
df['author'] = df['author'].replace(author_aliases)

# Exclude README.md for Cole Barbes before finding the most modified file
filtered_df = df[~((df['author'] == 'Cole Barbes') & (df['filePath'].str.contains('README.md', case=False)))]

# Group by author and aggregate data
result_df = df.groupby('author').agg(
    totalAdditions=('additions', 'sum'),
    totalDeletions=('deletions', 'sum'),
    netChanges=('netChanges', 'sum'),
    totalChanges=('totalChanges', 'sum'),
    filesChanged=('filesChanged', 'sum'),
    avgChangesPerCommit=('totalChanges', 'mean'),
    avgFilesChangedPerCommit=('filesChanged', 'mean'),
    maxChanges=('totalChanges', 'max'),
    minChanges=('totalChanges', 'min'),
    standardDeviationChanges=('totalChanges', 'std'),
    commitCount=('commitHash', 'nunique')
).reset_index()

# Find the most modified file using the filtered DataFrame
most_modified_file = filtered_df.groupby(['author', 'filePath']).size().reset_index(name='counts')
most_modified_file = most_modified_file.loc[most_modified_file.groupby('author')['counts'].idxmax()]

# Merge results with the main DataFrame
result_df = pd.merge(result_df, most_modified_file[['author', 'filePath']], on='author', how='left')
result_df.rename(columns={'filePath': 'mostModifiedFile'}, inplace=True)

# Write the result to an Excel file
result_df.to_excel('commit_analysis.xlsx', index=False)

# Print the result
print(result_df)