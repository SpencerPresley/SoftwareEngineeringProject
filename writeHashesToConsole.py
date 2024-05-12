import subprocess
import csv
import re

def get_commit_hashes():
    """Get commit hashes excluding merge commits."""
    cmd = ['git', 'log', '--pretty=format:%H', '--no-merges']
    output = subprocess.check_output(cmd).decode().strip()
    return output.split()

def get_commit_details(commit_hash):
    """Get details of a commit using the commit hash."""
    cmd = [
        'git', 'show', '--pretty=format:%an', '--numstat', commit_hash
    ]
    output = subprocess.check_output(cmd).decode().strip()
    return output

def parse_commit_details(details):
    """Parse the commit details and return the desired information."""
    lines = details.split('\n')
    author = lines[0]
    file_changes = []
    for line in lines[1:]:
        if line:
            additions, deletions, file_path = line.split('\t')
            file_changes.append({
                'additions': additions,
                'deletions': deletions,
                'file_path': file_path
            })
    return author, file_changes

def write_to_csv(data, filename='commit_details_without_bert.csv'):
    """Write the commit details to a CSV file."""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['author', 'commitHash', 'additions', 'deletions', 'filePath', 'filesChanged']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def should_include_file(file_path):
    """Check if a file should be included based on its path."""
    # Trim whitespace and convert to lower case for uniformity
    sanitized_path = file_path.strip().lower()
    
    # Debugging: print the path being checked
    print("Checking path:", sanitized_path)

    # Check for move operations and exclude them
    move_pattern = re.compile(r'\{.*?=>.*?\}')
    if move_pattern.search(sanitized_path):
        return False  # Exclude file paths that indicate a move operation

    # Using regular expressions to exclude paths
    # Exclude all file movements between 'package' and 'templates' directories except for 'ArticleAZ.html'
    exclude_pattern = re.compile(
        r'node_modules|json|stopwords|punkt|split_files|savedrecs\.txt|get-pip\.py|missing_abstracts\.txt|'
        r'frontend/static/javaoldcopy/|\.rtf|\.xml|\.csv|\.png|\.gv|'
        r'templates/unused_files/package\s+copy/style/|frontend/unused_files/|'
        r'frontend/templates/html/version2/|frontend/static/style/|'
        r'templates/unused_files/package\s+copy/html/|'
        r'\{frontend/package\s*=>\s*templates/unused_files/package\s+copy\}/java/|'
        r'frontend/package/style/styles\.css|'
        r'frontend/style/styles\.css|'
        r'fundev/|'
        r'\{fundev\s*=>\s*deprecated/fundev\}|'
        r'\{frontend/package\s*=>\s*templates\}/(html/faculty\.html|html/facultyaz\.html|html/topicaz\.html|html/index\.html|java/.*|style/.*|server\.js|unused_files/.*)|'
        r'frontend/templates/html/faculty\.html|'
        r'frontend/templates/html/facultyaz\.html|'
        r'frontend/templates/html/topicaz\.html|'
        r'frontend/templates/html/index\.html|'
        r'frontend/templates/html/article\.html|'
        r'frontend/templates/html/articleaz\.html|'
        r'webdev/mockups/articles-a-z/styles\.css|'  # Example kept
        r'frontend/package/html/article\.html|'
        r'frontend/package/html/articleaz\.html|'
        r'frontend/package/html/faculty\.html|'
        r'frontend/package/html/facultyaz\.html|'
        r'frontend/package/html/topicaz\.html|'
        r'frontend/package/html/index\.html|'
        r'textanalysis/test_bert\.ipynb', re.IGNORECASE)

    if exclude_pattern.search(sanitized_path):
        return False
    return True
# def should_include_file(file_path):
#     """Check if a file should be included based on its path."""
#     return (
#         'node_modules' not in file_path
#         and 'json' not in file_path.lower()
#         and 'stopwords' not in file_path.lower()
#         and 'punkt' not in file_path.lower()
#         and 'split_files' not in file_path.lower()
#         and 'savedrecs.txt' not in file_path.lower()
#         and 'get-pip.py' not in file_path.lower()
#         and 'missing_abstracts.txt' not in file_path.lower()
#         and 'FrontEnd/static/javaOldCopy/' not in file_path.strip().lower()
#         and not file_path.endswith('.rtf')
#         and not file_path.endswith('.xml')
#         and not file_path.endswith('.csv')
#         and not file_path.endswith(('.png', '.gv'))
#     )

if __name__ == '__main__':
    commit_hashes = get_commit_hashes()
    commit_data = []
    for commit_hash in commit_hashes:
        commit_details = get_commit_details(commit_hash)
        author, file_changes = parse_commit_details(commit_details)
        filtered_file_changes = [change for change in file_changes if should_include_file(change['file_path'])]
        files_changed = len(filtered_file_changes)
        for change in filtered_file_changes:
            commit_data.append({
                'author': author,
                'commitHash': commit_hash,
                'additions': change['additions'],
                'deletions': change['deletions'],
                'filePath': change['file_path'],
                'filesChanged': files_changed
            })
    write_to_csv(commit_data)
    print("Commit details have been written to 'commit_details_without_bert.csv'.")

