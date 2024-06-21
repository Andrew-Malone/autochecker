# Imposition Page Number Autochecker

This program takes two PDFs, an imposition and an imposition mock-up, extracts their page numbers, compares them, and then colorizes the pages in the imposition PDF based on whether or not the page numbers match.

## Basic Structure

1. Import the page imposition PDF
2. Calculate the mockup list based on the length of the PDF, printer, the FM and CVR offset, 8 pagers.
3. Extract the PDFs page list, compare, colorize the pages, output the modified pdf

## Functions

### `get_mockup_page_numbers`

- Caculate the page numbers
- Set the FM page numbers to roman numerals.
- Return a 2D list

### `compare_and_output`

- If the two lists are different lengths, alert that the number of sigs differs between the mock-up and actual imposition.
- Divide the actual imposition into eight sections, 4 each on the top and bottom, and extract the page numbers.
- Current regex: \b(?:[ivx]{1,4}|x{1,2})\b|\b\d{1,3}\b(?!\S)
- Get the 2D list:
  ```python
  [ [iv, 2, 4, 7], [6, 8, 9, 11], [0, x, 0, 0], [0, 0, 0, 0] ]
  ```
- Remove non-zero duplicates?
- Iterate through the sigs
  - Iterate through the pages, comparing mockup and actual
    - Set matches to green, 0s to grey, and non-matches to red
- Export the modified PDF
