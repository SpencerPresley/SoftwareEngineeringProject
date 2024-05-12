import subprocess
import csv
import os

def get_commit_hashes():
    """Get commit hashes from the main branch."""
    cmd = [
        'git', 'log', '--pretty=format:%H'
    ]
    hashes = subprocess.check_output(cmd).decode().split('\n')
    return hashes

def write_to_csv(hashes, filename='commit_hashes.csv'):
    """Write commit hashes to a CSV file."""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['commit_hash'])
        for hash in hashes:
            writer.writerow([hash])

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Change to the script's directory
    hashes = get_commit_hashes()
    write_to_csv(hashes)
    print("CSV file has been written successfully.")