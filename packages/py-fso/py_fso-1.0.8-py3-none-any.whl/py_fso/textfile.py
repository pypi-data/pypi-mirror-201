"""Some useful functions for working with a text file."""
import chardet
import os

def convert_to_utf8(file_path, initial_encoding=''):
    """
    Trying to convert a file into utf-8 encoding.

    :param file_path: a path (full or relative) to the file to convert
    :param initial_encoding: an initial file encoding
    :type file_path: string
    :type initial_encoding: string
    :return: None
    """
    with open(file_path, "rb") as F:
        text = F.read()
        if not initial_encoding:
            initial_encoding = chardet.detect(text).get("encoding")
        if initial_encoding and initial_encoding.lower() != "utf-8":
            try:
                text = text.decode(initial_encoding)
                text = text.encode("utf-8")
                with open(file_path, "wb") as f:
                    f.write(text)
                    print(file_path + " is successful converted.")
            except:
                print("There was error while converting " + file_path)
        else:
            print(file_path + " is already in " + initial_encoding + "encoding. No action needed.")


def split_into_certain_parts_amount(input_file, parts_amount, output_name='', file_encode='utf8'):
    """
    Split an input file into a certain amount of parts.

    :param input_file: a path (full or relative) to the file to split
    :param parts_amount: an amount of parts
    :param output_name: a path template (full or relative) of the resulting files, optional
    :param file_encode: an input file encoding
    :type input_file: string
    :type parts_amount: int
    :type output_name: string
    :type file_encode: string
    :return: None
    """
    if not output_name:
        output_name = input_file
    file_size = os.stat(input_file).st_size
    part_size = int(round(file_size / parts_amount, 0))
    input_file_handler = open(input_file, 'r', encoding=file_encode)
    chunk_number = 1
    already_written = 0
    while already_written < file_size:
        out_file_handler = open(output_name + os.extsep + str(chunk_number), 'w', encoding=file_encode)
        curr_chunk = input_file_handler.readlines(part_size)
        out_file_handler.writelines(curr_chunk)
        out_file_handler.close()
        already_written += len(('\n'.join(curr_chunk) + '\n').encode(file_encode))
        chunk_number += 1
    input_file_handler.close()


def split_into_parts_certain_size(input_file, part_size, output_name='', file_encode='utf8'):
    """
    Split an input file into parts of a certain size.

    :param input_file: a path (full or relative) to the file to split
    :param part_size: a size of the part
    :param output_name: a path template (full or relative) of the resulting files, optional
    :param file_encode: an input file encoding
    :type input_file: string
    :type part_size: int
    :type output_name: string
    :type file_encode: string
    :return: None
    """
    if not output_name:
        output_name = input_file
    file_size = os.stat(input_file).st_size
    input_file_handler = open(input_file, 'r', encoding=file_encode)
    chunk_number = 1
    already_written = 0
    while already_written < file_size:
        out_file_handler = open(output_name + os.extsep + str(chunk_number), 'w', encoding=file_encode)
        curr_chunk = input_file_handler.readlines(part_size)
        out_file_handler.writelines(curr_chunk)
        out_file_handler.close()
        already_written += len(('\n'.join(curr_chunk) + '\n').encode(file_encode))
        chunk_number += 1
    input_file_handler.close()
