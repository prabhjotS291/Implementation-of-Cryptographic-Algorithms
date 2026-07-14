import os
import numpy as np

# ==================================================
# CREATE OUTPUT DIRECTORY
# ==================================================

def create_output_directory(algorithm):

    path = os.path.join("output", algorithm)

    os.makedirs(path, exist_ok=True)

    return path


# ==================================================
# SAVE CIPHERTEXT
# ==================================================

def save_ciphertext(ciphertext, algorithm, extension):

    folder = create_output_directory(algorithm)

    filename = os.path.join(
        folder,
        f"encrypted{extension}"
    )

    if isinstance(ciphertext, np.ndarray):
        ciphertext = ciphertext.tobytes()

    elif isinstance(ciphertext, list):
        ciphertext = "".join(ciphertext).encode()

    with open(filename, "wb") as file:
        file.write(ciphertext)

    return filename


# ==================================================
# SAVE DECRYPTED FILE
# ==================================================

def save_decrypted_file(
    decrypted_bytes,
    algorithm,
    original_extension
):

    folder = create_output_directory(algorithm)

    filename = os.path.join(
        folder,
        f"decrypted{original_extension}"
    )

    if isinstance(decrypted_bytes, np.ndarray):
        decrypted_bytes = decrypted_bytes.tobytes()

    with open(filename, "wb") as file:
        file.write(decrypted_bytes)

    return filename


# ==================================================
# SAVE METRICS
# ==================================================

def save_metrics(metrics, algorithm):

    folder = create_output_directory(algorithm)

    filename = os.path.join(
        folder,
        "metrics.txt"
    )

    with open(filename, "w") as file:

        file.write("=" * 45 + "\n")
        file.write(f"{algorithm} RESULTS\n")
        file.write("=" * 45 + "\n\n")

        for key, value in metrics.items():

            file.write(f"{key:<25}: {value}\n")

    return filename