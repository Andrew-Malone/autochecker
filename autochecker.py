import fitz  # PyMuPDF

def extract_text_from_top_and_bottom_twentieth(pdf_path, output_file):
    with open(output_file, "w", encoding="utf-8") as f_out:
        doc = fitz.open(pdf_path)
        
        # Iterate through each page
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_height = page.rect.height  # Get page height
            
            # Calculate the height of the top 1/20th and bottom 1/20th of the page
            twentieth_height = page_height / 20
            
            # Define the rectangles for the top 1/20th and bottom 1/20th of the page
            top_twentieth_rect = fitz.Rect(0, 0, page.rect.width, twentieth_height)
            bottom_twentieth_rect = fitz.Rect(0, page_height - twentieth_height, page.rect.width, page_height)
            
            # Get the text within the top 1/20th of the page
            top_text = page.get_text("text", clip=top_twentieth_rect)
            # Get the text within the bottom 1/20th of the page
            bottom_text = page.get_text("text", clip=bottom_twentieth_rect)
            
            # Write the extracted text to the output file
            f_out.write(f"Top 1/20th of page {page_num + 1}:\n")
            f_out.write(top_text + "\n\n")
            f_out.write(f"Bottom 1/20th of page {page_num + 1}:\n")
            f_out.write(bottom_text + "\n\n")
            
        doc.close()

# Example usage
pdf_path = "test.pdf"
output_file = "output.txt"
extract_text_from_top_and_bottom_twentieth(pdf_path, output_file)
