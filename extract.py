import fitz
import re

# Return a single match from extracted text
def extract_numbers_from_text(text):
    pattern = r'\b(?:[ivx]{1,4}|x{1,2})\b|\b\d{1,3}\b(?!\S)'
    matches = re.findall(pattern, text)

    if matches:
        # If there's one match, return it
        if len(matches) == 1:
            return matches[0]
        # If there are multiple matches, return the first non-digit match,
        # or the largest integer match if there are no non-digit matches
        else:
            non_digit_matches = [match for match in matches if not match.isdigit()]
            if non_digit_matches:
                return non_digit_matches[0]
            else:
                return max([int(match) for match in matches])
    else:
        return 0

def extract_page_numbers(pdf_path, output_file):
    with open(output_file, "w", encoding="utf-8") as f_out:
        doc = fitz.open(pdf_path)
        main_container = []
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_height = page.rect.height
            page_width = page.rect.width
            twentieth_height = page_height / 20
            
            # Define the smaller rectangles for the top and bottom sections
            top_rectangles = [
                fitz.Rect(0, 0, page_width / 4, twentieth_height),
                fitz.Rect(page_width / 4, 0, page_width / 2, twentieth_height),
                fitz.Rect(page_width / 2, 0, 3 * page_width / 4, twentieth_height),
                fitz.Rect(3 * page_width / 4, 0, page_width, twentieth_height)
            ]
            bottom_rectangles = [
                fitz.Rect(0, page_height - twentieth_height, page_width / 4, page_height),
                fitz.Rect(page_width / 4, page_height - twentieth_height, page_width / 2, page_height),
                fitz.Rect(page_width / 2, page_height - twentieth_height, 3 * page_width / 4, page_height),
                fitz.Rect(3 * page_width / 4, page_height - twentieth_height, page_width, page_height)
            ]
            
            # Draw red borders around the smaller rectangles
            for rect in top_rectangles + bottom_rectangles:
                page.draw_rect(rect, color=(1, 0, 0), width=2)
            
            # Write the raw output text to the output file, deliniated by rectangle and sig number
            # code here

            # Extract text from top and bottom rectangles, and extract numbers
            sig_container = []
            top_list = []
            bottom_list = []
            
            for rect in top_rectangles:
                top_list.append(extract_numbers_from_text(page.get_text("text", clip=rect)))
            for rect in bottom_rectangles:
                bottom_list.append(extract_numbers_from_text(page.get_text("text", clip=rect)))    

            sig_container.append(top_list)
            sig_container.append(bottom_list)
            main_container.append(sig_container)

            
        # Save the modified PDF with the red borders
        doc.save("output_with_borders.pdf")
        doc.close()
        return main_container

# Test
pdf_path = "242807_352918_1.pdf"
output_file = "output.txt"
print(extract_page_numbers(pdf_path, output_file))
