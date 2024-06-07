# PDF Page Number Comparison and Colorization

This program takes two PDFs, an imposition and an imposition mock-up, extracts their page numbers, compares them, and then colorizes the pages in the imposition PDF based on whether or not the page numbers match.

## Main

1. Import both PDFs
2. Get offset (preceding cover pages + FM pages)
3. `actual_list` = get_actual_page_numbers()
4. `mockup_list` = get_mockup_page_numbers(offset)
5. `compare_and_output(actual_list, mockup_list)`

## Functions

### `get_actual_page_numbers`

- Divide the actual imposition into eight sections, 4 each on the top and bottom, and extract the page numbers from those sections.
- Return a 2D list:
  ```python
  [ [iv, 2, 4, 7], [6, 8, 9, 11], [x, x, 0, x], [x, x, x, x] ]
  ```

### `get_mockup_page_numbers(offset)`

- Get the page numbers from the imposition mock-up
  - Extract the numbers, set the FM pages, subtract the offset from the rest
- Return a 2D list

### `colorize(sig_number, color)`

- Surround a sig with a border depending on its status:
  - Green: numbers match
  - Grey: uncertain/missing numbers
  - Red: numbers don't match
- Eventually improve the function to colorize the borders of individual pages

### `compare_and_output(actual_list, mockup_list)`

1. If the two lists are different lengths, alert that the number of sigs differs between the mock-up and imposition.
2. Set `status_color` to GREEN.
3. For each sig in the actual list:
   - For each page in the sig:
      - If `actual_page_number == 0`, set `status_color` to GREY.
      - Else if `actual_list[sig_number][actual_page] != mockup_list[sig_number][mockup_page]`, set `status_color` to RED.
   - Call `colorize(sig_number, status_color)` to apply the color.
4. Export the colorized PDF.
