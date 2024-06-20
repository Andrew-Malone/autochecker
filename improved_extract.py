import fitz
import re

# Compile the regex pattern
pattern = re.compile(r'\b(?:[ivx]{1,4}|x{1,2})\b|\b\d{1,3}\b(?!\S)')

# Return a single match from extracted text
def extract_numbers_from_text(text):
    matches = pattern.findall(text)

    if matches:
        # If there's one match, return it
        if len(matches) == 1:
            return matches[0]
        # If there are multiple matches, return the first non-digit match,
        # or the largest integer match if there are no non-digit matches
        non_digit_matches = [match for match in matches if not match.isdigit()]
        if non_digit_matches:
            return non_digit_matches[0]
        else:
            return max(matches, key=int)
    else:
        return '0'

def extract_page_numbers(pdf_path, output_file):
    mockup = [
        [['0', '0', '0', '0'], ['0', '0', '0', '0']],
        [['0', '0', '0', '0'], ['0', '0', '0', '0']],
        [['7', 'iv', 'i', '10'], ['6', 'v', '2', '3']],
        [['9', '0', 'iii', '8'], ['4', '1', 'vi', '5']],
        [['23', '14', '11', '26'], ['22', '15', '18', '19']],
        [['25', '12', '13', '24'], ['20', '17', '16', '21']],
        [['39', '30', '27', '42'], ['38', '31', '34', '35']],
        [['41', '28', '29', '40'], ['36', '33', '32', '37']],
        [['55', '46', '43', '58'], ['54', '47', '50', '51']],
        [['57', '44', '45', '56'], ['52', '49', '48', '53']],
        [['71', '62', '59', '74'], ['70', '63', '66', '67']],
        [['73', '60', '61', '72'], ['68', '65', '64', '69']],
        [['87', '78', '75', '90'], ['86', 'i', '82', '83']],
        [['89', '76', '77', '88'], ['84', '81', '80', '85']],
        [['103', '94', '91', '106'], ['102', '95', '98', '99']],
        [['105', '92', '93', '104'], ['100', '97', '96', '101']],
        [['119', '110', '107', '122'], ['118', '111', '114', '115']],
        [['121', '108', '109', '120'], ['116', '113', '112', '117']],
        [['135', '126', '123', '138'], ['134', '127', '130', '131']],
        [['137', '124', '125', '136'], ['132', '129', 'i', '133']],
        [['151', '142', '139', '154'], ['150', '143', '146', '147']],
        [['153', '140', '141', '152'], ['148', '145', '144', '149']],
        [['167', '158', '155', '170'], ['166', '159', '162', '163']],
        [['169', '156', '157', '168'], ['164', '161', '160', '165']],
        [['183', '174', '171', '186'], ['182', '175', '178', '179']],
        [['185', '172', '173', '184'], ['180', '177', '176', '181']],
        [['199', '190', '187', '202'], ['198', '191', '194', '195']],
        [['201', '188', '189', '200'], ['196', '193', '192', '197']],
        [['215', '206', '203', '218'], ['214', '207', '210', '211']],
        [['217', '204', '205', '216'], ['212', '209', '208', '213']],
        [['231', '222', '219', '234'], ['230', '223', '226', '227']],
        [['233', '220', '221', '232'], ['228', '225', '224', '229']],
        [['247', '238', '235', '250'], ['246', '239', '242', '243']],
        [['249', '236', '237', '248'], ['244', '241', '240', '245']],
        [['263', '254', '251', '266'], ['262', '255', '258', '259']],
        [['265', '252', '253', '264'], ['260', '257', '256', '261']],
        [['279', '270', '267', '282'], ['278', '271', '274', '275']],
        [['281', '268', '269', '280'], ['276', '273', '272', '277']],
        [['295', '286', '283', '10'], ['294', '287', '290', '291']],
        [['297', '284', '285', '296'], ['292', '289', '288', '293']]
    ]

    with open(output_file, "w", encoding="utf-8") as f_out:
        doc = fitz.open(pdf_path)
        main_container = []

        for page_num, page in enumerate(doc):
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

            # Extract text from top and bottom rectangles, and extract numbers
            sig_container = [
                [extract_numbers_from_text(page.get_text("text", clip=rect)) for rect in top_rectangles],
                [extract_numbers_from_text(page.get_text("text", clip=rect)) for rect in bottom_rectangles]
            ]
            main_container.append(sig_container)

            # Write the raw output text to the output file
            for rect_index, rect in enumerate(top_rectangles + bottom_rectangles):
                text = page.get_text("text", clip=rect)
                f_out.write(f"SIG {page_num + 1}, RECTANGLE {rect_index + 1}:\n{text}")

            # Compare mockup with sig container and color borders and add text
            def draw_comparison(page, mockup_value, sig_value, rect):
                if mockup_value != sig_value:
                    color = (0.5, 0.5, 0.5) if sig_value == '0' else (1, 0, 0)
                else:
                    color = (0, 1, 0)

                page.draw_rect(rect, color=color, width=6)

                # Position the text in the middle of the rectangle
                text_x = (rect.x0 + rect.x1) / 2
                text_y = (rect.y0 + rect.y1) / 2
                font_size = 40

                # Draw the mockup number in black
                page.insert_text((text_x - 20, text_y - 10), str(mockup_value) + '-', fontsize=font_size, color=(0, 0, 0))
                # Draw the sig number in the same color as the rectangle border
                page.insert_text((text_x + 20, text_y - 10), str(sig_value), fontsize=font_size, color=color)

            for mockup_top, sig_top, rect in zip(mockup[page_num][0], sig_container[0], top_rectangles):
                draw_comparison(page, mockup_top, sig_top, rect)

            for mockup_bottom, sig_bottom, rect in zip(mockup[page_num][1], sig_container[1], bottom_rectangles):
                draw_comparison(page, mockup_bottom, sig_bottom, rect)

            print(f"Sig {page_num + 1} completed processing...")

        # Save the modified PDF with the red borders
        doc.save("output_with_borders.pdf")
        doc.close()
        return main_container

# Test
pdf_path = "242807_352918_1.pdf"
output_file = "output.txt"
print(extract_page_numbers(pdf_path, output_file))
