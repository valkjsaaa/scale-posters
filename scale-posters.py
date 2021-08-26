import argparse

import PyPDF3
import tqdm

parser = argparse.ArgumentParser("Scale posters to have the same width")
parser.add_argument("--input", help="input posters PDF", required=True)
parser.add_argument("--output", help="output posters PDF", required=True)
args = parser.parse_args()

input_file = open(args.input, "rb")
output_file = open(args.output, "wb")
pdf_reader = PyPDF3.PdfFileReader(input_file)
pdf_writer = PyPDF3.PdfFileWriter()


def poster_width(page):
    return page.mediaBox[2] - page.mediaBox[0]


target_width = max([poster_width(page) for page in pdf_reader.pages])

for page in tqdm.tqdm(pdf_reader.pages):
    page_width = poster_width(page)
    page.scaleBy(float(target_width / page_width))
    page.cropBox = page.mediaBox
    page.bleedBox = page.mediaBox
    page.trimBox = page.mediaBox
    page.artBox = page.mediaBox
    pdf_writer.addPage(page)

pdf_writer.write(output_file)

input_file.close()
output_file.close()
