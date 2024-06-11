# Imposition Page Number Autochecker

This program takes two PDFs, an imposition and an imposition mock-up, extracts their page numbers, compares them, and then colorizes the pages in the imposition PDF based on whether or not the page numbers match.

## Main

1. Import both PDFs
2. Get the mockup list minus the offset
3. Get the actual list and colorize the pages
4. Output the modified pdf

## Functions

### `get_mockup_page_numbers`

- Get the offset
- Get the page numbers from the imposition mock-up
- Subtract the offset, set the negatives to the FM roman numerals
- Return a 2D list

### `compare_and_output()`

- If the two lists are different lengths, alert that the number of sigs differs between the mock-up and actual imposition.
- Divide the actual imposition into eight sections, 4 each on the top and bottom, and extract the page numbers from those sections:
  ```python
  [ [iv, 2, 4, 7], [6, 8, 9, 11], [x, x, 0, x], [x, x, x, x] ]
  ```
-Iterate through the sigs
 -Iterate through the pages, comparing mockup and actual
   -Set matches to green, 0s to grey, and non-matches to red
- Export the modified PDF
