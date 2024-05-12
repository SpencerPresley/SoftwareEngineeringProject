#!/bin/bash

# Create a temporary file to store commit logs
temp_file="temp_commit_logs.txt"

# Get all unique branches
branches=$(git branch -r | grep -v HEAD | sed 's/origin\///g')

# Prepare the commit log file
echo "\"Branch\",\"Commit SHA\",\"Author\",\"Date\",\"Message\"" > $temp_file

# Loop through all branches
for branch in $branches; do
    git checkout $branch > /dev/null 2>&1
    # List commits and ensure special characters in messages are escaped
    git log --no-merges --pretty=format:"\"$branch\",\"%H\",\"%an\",\"%ad\",\"%s\"" -- . ':(exclude)**/node_modules' ':(exclude)**/*.json' | \
    sed 's/"/\\"/g' | sed 's/,/\\,/g' | sed 's/%/%%/g' >> $temp_file
done

# Use Python to create an Excel file from the log data
# Use Python to create an Excel file from the log data
python3 << END
import pandas as pd

try:
    # Load the data into a DataFrame
    data = pd.read_csv("$temp_file", quotechar='"', escapechar='\\\\', doublequote=True)
    # Create an Excel writer
    writer = pd.ExcelWriter('Commit_Report.xlsx', engine='openpyxl')
    # Write your DataFrame to an Excel sheet
    data.to_excel(writer, sheet_name='Commits', index=False)
    # Save the Excel file
    writer.close()  # Correct method to finalize and save the file
    print("Excel file created successfully.")
except Exception as e:
    print(f"An error occurred: {e}")

END

# Clean up
rm $temp_file