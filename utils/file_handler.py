import os
import numpy as np

def load_file(file_path):
    """
    Reads any file and returns its raw bytes along with
    useful metadata.

    Parameters:
        file_path (str): Path to the input file.

    Returns:
        plaintext_bytes (numpy.ndarray): File as uint8 array.
        file_info (dict): Metadata about the file.
    """
    with open(file_path, 'rb') as file:
        raw_bytes = file.read()

    plaintext_bytes = np.frombuffer(raw_bytes, dtype=np.uint8)

    file_info = {
        'path': file_path,
        'name': os.path.basename(file_path),
        'extension': os.path.splitext(file_path)[1],
        'size_bytes': len(raw_bytes),
        'size_mb': len(raw_bytes) / (1024 * 1024)
    }

    return plaintext_bytes, file_info