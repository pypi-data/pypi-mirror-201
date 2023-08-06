import tensorflow as tf
import argparse
from magstoolnewversion import BatchCheck


def run():
    parser = argparse.ArgumentParser(description='Process some PDF data.')
    parser.add_argument('input_pdf_folder', metavar='input_pdf_folder', type=str,
                        help='path to folder containing PDF files to process')

    args = parser.parse_args()
    print(args.input_pdf_folder)

    BatchCheck.main(args.input_pdf_folder)

