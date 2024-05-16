import csv
import os

def clean_csv(file_path):
    updated_file_path = os.path.splitext(file_path)[0] + "-updated.csv"
    
    with open(file_path, mode='r', newline='', encoding='utf-8') as infile, \
         open(updated_file_path, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        headers = next(reader)  # Read the header row
        writer.writerow(headers)  # Write the header row to the new file
        
        for row in reader:
            if row:
                first_element = row[0].strip()
                
                # Remove surrounding quotes from the first element if present
                if first_element.startswith('"') and first_element.endswith('"'):
                    first_element = first_element[1:-1].strip()
                
                # If the first element is empty, skip the row
                if first_element:
                    # Update the row with the cleaned first element
                    row[0] = first_element
                    writer.writerow(row)
    
    print(f"Cleaned CSV saved to {updated_file_path}")

# Example usage
csv_path = "csv-files/FIG-HB.csv"
clean_csv(csv_path)
