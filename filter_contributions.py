import pandas as pd

def filter_contributions(input_csv, output_csv):
    # Load the CSV file
    data = pd.read_csv(input_csv, header=None, names=['additions', 'deletions', 'file_path', 'commit_hash', 'author', 'email', 'date'])
    print(data.head())
    input("Press Enter to continue...")

    # Normalize the data by stripping any unwanted spaces and filling NA values
    data['file_path'] = data['file_path'].str.strip().fillna('')
    data['commit_hash'] = data['commit_hash'].str.strip()

    # Find all commits that involve node_modules
    node_modules_commits = set(data[data['file_path'].str.contains('node_modules', na=False)]['commit_hash'])
    print(f"Found {len(node_modules_commits)} commits to exclude.")

    # Filter out the rows with commits that are in the node_modules_commits set
    clean_data = data[~data['commit_hash'].isin(node_modules_commits)]

    # Save the clean data to a new CSV file
    clean_data.to_csv(output_csv, index=False)
    print(f"Clean report saved as '{output_csv}'.")

# Specify the input and output CSV file names
input_csv = 'contributions.csv'
output_csv = 'clean_contributions.csv'

# Call the function to filter contributions
filter_contributions(input_csv, output_csv)