import fitz
import re

def extract_numbers_from_text(text):
    pattern = r'\b(?:[ivx]{1,4}|x{1,2})\b|\b\d{1,3}\b(?!\S)'
    matches = re.findall(pattern, text)

    return matches

def extract_page_numbers(pdf_path, output_file):
    with open(output_file, "w", encoding="utf-8") as f_out:
        doc = fitz.open(pdf_path)
        page_numbers_list = []
        
        # Iterate through each page
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_height = page.rect.height  # Get sig page height
            page_numbers = []
            
            # Calculate the height of the top 1/20th and bottom 1/20th of the sig
            twentieth_height = page_height / 20
            
            # Define the rectangles for the top 1/20th and bottom 1/20th of the sig
            top_twentieth_rect = fitz.Rect(0, 0, page.rect.width, twentieth_height)
            bottom_twentieth_rect = fitz.Rect(0, page_height - twentieth_height, page.rect.width, page_height)
            
            # Get the text within the top 1/20th and bottom 1/20th of the sig
            top_text = page.get_text("text", clip=top_twentieth_rect)
            bottom_text = page.get_text("text", clip=bottom_twentieth_rect)

            # Remove one space following letters that are not x, i, or v
            top_text = re.sub(r'(?<![xiv])(?<=[a-zA-Z]) ', '', top_text)
            bottom_text = re.sub(r'(?<![xiv])(?<=[a-zA-Z]) ', '', bottom_text)
            
            # Extract numbers from the top and bottom text
            top_numbers = extract_numbers_from_text(top_text)
            bottom_numbers = extract_numbers_from_text(bottom_text)
            
            # Create a 2D array for each sig's numbers and append to the list
            page_numbers = [top_numbers, bottom_numbers]
            page_numbers_list.append(page_numbers)

            # Write the output text to the output file
            f_out.write(f"TOP 1/20th OF SIG {page_num + 1}:\n")
            f_out.write(top_text)
            f_out.write(f"BOTTOM 1/20th OF SIG {page_num + 1}:\n")
            f_out.write(bottom_text)
            
        doc.close()
        return page_numbers_list

# Test
pdf_path = "test2.pdf"
output_file = "output.txt"
page_numbers_list = extract_page_numbers(pdf_path, output_file)
print(page_numbers_list)
