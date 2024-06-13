# Imposition Page Number Autochecker

This program takes two PDFs, an imposition and an imposition mock-up, extracts their page numbers, compares them, and then colorizes the pages in the imposition PDF based on whether or not the page numbers match.

## Basic Structure

1. Import both PDFs
2. Get the mockup list (minus the FM and CVR offset, roman numerals set for FM pages appropriately)
3. Get the actual list, compare, colorize the pages, output the modified pdf

## Functions

### `get_mockup_page_numbers`

- Get the offset
- Get the page numbers from the imposition mock-up
- Subtract the offset, set the negatives to the FM roman numerals
- Return a 2D list

### `compare_and_output()`

- If the two lists are different lengths, alert that the number of sigs differs between the mock-up and actual imposition.
- Divide the actual imposition into eight sections, 4 each on the top and bottom, and extract the page numbers.
- Possible regex: (?<=^|\s)(i|ii|iii|iv|v|vi|vii|viii|ix|x|xi|xii|xiii|xiv|xv|xvi|xvii|xviii|xix|xx|xxi|xxii|xxiii|xxiv|xxv|xxvi|xxvii|xxviii|xxix|xxx|\b[1-9]\b|\b[1-9][0-9]\b|\b[1-9][0-9][0-9]\b)(?=\s|$)
- Get the 2D list:
  ```python
  [ [iv, 2, 4, 7], [6, 8, 9, 11], [x, x, 0, x], [x, x, x, x] ]
  ```
- Iterate through the sigs
  - Iterate through the pages, comparing mockup and actual
    - Set matches to green, 0s to grey, and non-matches to red
- Export the modified PDF
