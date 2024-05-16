from PIL import Image
import pdfplumber
import csv
import re


def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text_data = []
        for page in pdf.pages:
            table = page.extract_table()
            text_data.append(table)
    return text_data


def extract_table_from_n_page(pdf_path,page_number):
    with pdfplumber.open(pdf_path) as pdf:
        text_data=pdf.pages[page_number].extract_table()
    return text_data

        
def parse_table_data(table_data, event):
    skills = []
    element_group = ""
    difficulty_headers = table_data[0]
    roman_to_int = {'I': '1', 'II': '2', 'III': '3', 'IV': '4', 'V': '5', 'VI': '6', 'VII': '7', 'VIII': '8', 'IX': '9', 'X': '10'}
    
    for row in table_data[1:]:  # Skip header row
        if row[0] and "EG" in row[0]:
            element_group_match = re.search(r'EG\s(\w+)', row[0])
            if element_group_match:
                element_group = element_group_match.group(1).strip()
                element_group = roman_to_int.get(element_group, element_group)
        for i, cell in enumerate(row):
            if cell:
                # Remove newline characters and ensure there is a space after the period
                cell = re.sub(r'\n', ' ', cell).strip()
                cell = re.sub(r'(\d+)\.(?! )', r'\1. ', cell)

                match = re.match(r'(\d+)\.\s*(.+)', cell)
                if match:
                    skill_name = match.group(2).strip()
                    difficulty = difficulty_headers[i].split('=')[-1].strip() if difficulty_headers[i] and '=' in difficulty_headers[i] else ""
                    skills.append([skill_name, element_group, difficulty, event])
                
    return skills

def save_to_csv(skills, csv_path):
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Skill Name', 'Element Group', 'Difficulty', 'Event'])
        writer.writerows(skills)

def populateAll():
    # Example usage
    pdf_path = "pdf-files/hb.pdf"
    csv_path = "csv-files/FIG-HB.csv"
    event = "HB"  # Replace with actual event name

    table_data = extract_text_from_pdf(pdf_path)
    all_skills = []
    for page_data in table_data:
        if page_data:  # Check if page_data is not None or empty
            skills = parse_table_data(page_data, event)
            all_skills.extend(skills)

    save_to_csv(all_skills, csv_path)

    print(f"Skills extracted and saved to {csv_path}")

populateAll()

# print(extract_table_from_n_page('fx.pdf',9))


