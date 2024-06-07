This program takes two pdfs, an imposition and a imposition mock-up, extracts their page numbers, compares them,
and then colorizes the pages in the imposition pdf based on whether or not the pages numbers match.

MAIN

  import both pdfs

  get offset (precending cover pages + FM pages)

  actual_list = get_actual_page_numbers
  mockup_list = get_mockup_page_numbers(offset)

  compare_and_output(2 lists)
  


FUNCTIONS

get_actual_page_numbers 
  // Divide the actual imposition into eight sections, 4 each on the top and bottom, and extract the page numbers from those sections.
  // Return a 2d list [ [iv, 2, 4, 7], [6,8,9 11], [x, x, 0, x], [x, x, x, x] ]

get_mockup_page_numbers(int offset)
  // Get the page numbers from the imposition mock-up
    // Extract the numbers, set the FM pages, subtract the offset from the rest
  // Return a 2d list

colorize(sig number, color)
  // Surround a sig with a border depending on its status (Green - numbers match, Grey - uncertain/missing numbers, Red = numbers don't match)
  // Eventually improve the function to colorize the borders of individual pages

compare_and_output(actual_list, mockup_list)
  
   if the two lists are different lengths
     alert (the number of sigs differs between the mock-up and imposition)

   status_color = GREEN

   for(sig in actual list)
   {
      for(page in sig)
         //check if the pages don't match and the actual page number is 0 (blank/unknown)
         if(actual_page_number == 0)
            status_color = GREY
          else(actual_list[sig_number][actual_page] != actual_list[sig_number][mockup_page])
            status_color = RED
  
      colorize(sig_number, status_color)
    }

    export the colorized pdf
