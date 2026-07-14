import os
import numpy as np

from utils.file_handler import load_file

from utils.metrics import (
    calculate_entropy,
    calculate_avalanche,
    calculate_throughput,
    calculate_encryption_ratio,
    verify,
    flip_first_bit
)

from utils.benchmark import (
    benchmark,
    Benchmark
)

from utils.save_files import (
    save_ciphertext,
    save_decrypted_file,
    save_metrics
)

# ==================================================
# CONFIGURATION
# ==================================================

INPUT_FILE = os.path.join("input", "image.png")
NUM_RUNS = 10


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def num_to_dna(arr):

    dna = ['A', 'C', 'G', 'T']

    return [dna[num] for num in arr]


def reconstruct_bytes(arr, index):

    return (
        (arr[index * 4] << 6)
        | (arr[index * 4 + 1] << 4)
        | (arr[index * 4 + 2] << 2)
        | arr[index * 4 + 3]
    )


# ==================================================
# LOOKUP TABLE
# ==================================================

lookup = [
    [0, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 2],
    [0, 0, 0, 3],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 1, 2],
    [0, 0, 1, 3],
    [0, 0, 2, 0],
    [0, 0, 2, 1],
    [0, 0, 2, 2],
    [0, 0, 2, 3],
    [0, 0, 3, 0],
    [0, 0, 3, 1],
    [0, 0, 3, 2],
    [0, 0, 3, 3],
    [0, 1, 0, 0],
    [0, 1, 0, 1],
    [0, 1, 0, 2],
    [0, 1, 0, 3],
    [0, 1, 1, 0],
    [0, 1, 1, 1],
    [0, 1, 1, 2],
    [0, 1, 1, 3],
    [0, 1, 2, 0],
    [0, 1, 2, 1],
    [0, 1, 2, 2],
    [0, 1, 2, 3],
    [0, 1, 3, 0],
    [0, 1, 3, 1],
    [0, 1, 3, 2],
    [0, 1, 3, 3],
    [0, 2, 0, 0],
    [0, 2, 0, 1],
    [0, 2, 0, 2],
    [0, 2, 0, 3],
    [0, 2, 1, 0],
    [0, 2, 1, 1],
    [0, 2, 1, 2],
    [0, 2, 1, 3],
    [0, 2, 2, 0],
    [0, 2, 2, 1],
    [0, 2, 2, 2],
    [0, 2, 2, 3],
    [0, 2, 3, 0],
    [0, 2, 3, 1],
    [0, 2, 3, 2],
    [0, 2, 3, 3],
    [0, 3, 0, 0],
    [0, 3, 0, 1],
    [0, 3, 0, 2],
    [0, 3, 0, 3],
    [0, 3, 1, 0],
    [0, 3, 1, 1],
    [0, 3, 1, 2],
    [0, 3, 1, 3],
    [0, 3, 2, 0],
    [0, 3, 2, 1],
    [0, 3, 2, 2],
    [0, 3, 2, 3],
    [0, 3, 3, 0],
    [0, 3, 3, 1],
    [0, 3, 3, 2],
    [0, 3, 3, 3],
    [1, 0, 0, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 2],
    [1, 0, 0, 3],
    [1, 0, 1, 0],
    [1, 0, 1, 1],
    [1, 0, 1, 2],
    [1, 0, 1, 3],
    [1, 0, 2, 0],
    [1, 0, 2, 1],
    [1, 0, 2, 2],
    [1, 0, 2, 3],
    [1, 0, 3, 0],
    [1, 0, 3, 1],
    [1, 0, 3, 2],
    [1, 0, 3, 3],
    [1, 1, 0, 0],
    [1, 1, 0, 1],
    [1, 1, 0, 2],
    [1, 1, 0, 3],
    [1, 1, 1, 0],
    [1, 1, 1, 1],
    [1, 1, 1, 2],
    [1, 1, 1, 3],
    [1, 1, 2, 0],
    [1, 1, 2, 1],
    [1, 1, 2, 2],
    [1, 1, 2, 3],
    [1, 1, 3, 0],
    [1, 1, 3, 1],
    [1, 1, 3, 2],
    [1, 1, 3, 3],
    [1, 2, 0, 0],
    [1, 2, 0, 1],
    [1, 2, 0, 2],
    [1, 2, 0, 3],
    [1, 2, 1, 0],
    [1, 2, 1, 1],
    [1, 2, 1, 2],
    [1, 2, 1, 3],
    [1, 2, 2, 0],
    [1, 2, 2, 1],
    [1, 2, 2, 2],
    [1, 2, 2, 3],
    [1, 2, 3, 0],
    [1, 2, 3, 1],
    [1, 2, 3, 2],
    [1, 2, 3, 3],
    [1, 3, 0, 0],
    [1, 3, 0, 1],
    [1, 3, 0, 2],
    [1, 3, 0, 3],
    [1, 3, 1, 0],
    [1, 3, 1, 1],
    [1, 3, 1, 2],
    [1, 3, 1, 3],
    [1, 3, 2, 0],
    [1, 3, 2, 1],
    [1, 3, 2, 2],
    [1, 3, 2, 3],
    [1, 3, 3, 0],
    [1, 3, 3, 1],
    [1, 3, 3, 2],
    [1, 3, 3, 3],
    [2, 0, 0, 0],
    [2, 0, 0, 1],
    [2, 0, 0, 2],
    [2, 0, 0, 3],
    [2, 0, 1, 0],
    [2, 0, 1, 1],
    [2, 0, 1, 2],
    [2, 0, 1, 3],
    [2, 0, 2, 0],
    [2, 0, 2, 1],
    [2, 0, 2, 2],
    [2, 0, 2, 3],
    [2, 0, 3, 0],
    [2, 0, 3, 1],
    [2, 0, 3, 2],
    [2, 0, 3, 3],
    [2, 1, 0, 0],
    [2, 1, 0, 1],
    [2, 1, 0, 2],
    [2, 1, 0, 3],
    [2, 1, 1, 0],
    [2, 1, 1, 1],
    [2, 1, 1, 2],
    [2, 1, 1, 3],
    [2, 1, 2, 0],
    [2, 1, 2, 1],
    [2, 1, 2, 2],
    [2, 1, 2, 3],
    [2, 1, 3, 0],
    [2, 1, 3, 1],
    [2, 1, 3, 2],
    [2, 1, 3, 3],
    [2, 2, 0, 0],
    [2, 2, 0, 1],
    [2, 2, 0, 2],
    [2, 2, 0, 3],
    [2, 2, 1, 0],
    [2, 2, 1, 1],
    [2, 2, 1, 2],
    [2, 2, 1, 3],
    [2, 2, 2, 0],
    [2, 2, 2, 1],
    [2, 2, 2, 2],
    [2, 2, 2, 3],
    [2, 2, 3, 0],
    [2, 2, 3, 1],
    [2, 2, 3, 2],
    [2, 2, 3, 3],
    [2, 3, 0, 0],
    [2, 3, 0, 1],
    [2, 3, 0, 2],
    [2, 3, 0, 3],
    [2, 3, 1, 0],
    [2, 3, 1, 1],
    [2, 3, 1, 2],
    [2, 3, 1, 3],
    [2, 3, 2, 0],
    [2, 3, 2, 1],
    [2, 3, 2, 2],
    [2, 3, 2, 3],
    [2, 3, 3, 0],
    [2, 3, 3, 1],
    [2, 3, 3, 2],
    [2, 3, 3, 3],
    [3, 0, 0, 0],
    [3, 0, 0, 1],
    [3, 0, 0, 2],
    [3, 0, 0, 3],
    [3, 0, 1, 0],
    [3, 0, 1, 1],
    [3, 0, 1, 2],
    [3, 0, 1, 3],
    [3, 0, 2, 0],
    [3, 0, 2, 1],
    [3, 0, 2, 2],
    [3, 0, 2, 3],
    [3, 0, 3, 0],
    [3, 0, 3, 1],
    [3, 0, 3, 2],
    [3, 0, 3, 3],
    [3, 1, 0, 0],
    [3, 1, 0, 1],
    [3, 1, 0, 2],
    [3, 1, 0, 3],
    [3, 1, 1, 0],
    [3, 1, 1, 1],
    [3, 1, 1, 2],
    [3, 1, 1, 3],
    [3, 1, 2, 0],
    [3, 1, 2, 1],
    [3, 1, 2, 2],
    [3, 1, 2, 3],
    [3, 1, 3, 0],
    [3, 1, 3, 1],
    [3, 1, 3, 2],
    [3, 1, 3, 3],
    [3, 2, 0, 0],
    [3, 2, 0, 1],
    [3, 2, 0, 2],
    [3, 2, 0, 3],
    [3, 2, 1, 0],
    [3, 2, 1, 1],
    [3, 2, 1, 2],
    [3, 2, 1, 3],
    [3, 2, 2, 0],
    [3, 2, 2, 1],
    [3, 2, 2, 2],
    [3, 2, 2, 3],
    [3, 2, 3, 0],
    [3, 2, 3, 1],
    [3, 2, 3, 2],
    [3, 2, 3, 3],
    [3, 3, 0, 0],
    [3, 3, 0, 1],
    [3, 3, 0, 2],
    [3, 3, 0, 3],
    [3, 3, 1, 0],
    [3, 3, 1, 1],
    [3, 3, 1, 2],
    [3, 3, 1, 3],
    [3, 3, 2, 0],
    [3, 3, 2, 1],
    [3, 3, 2, 2],
    [3, 3, 2, 3],
    [3, 3, 3, 0],
    [3, 3, 3, 1],
    [3, 3, 3, 2],
    [3, 3, 3, 3]
]


# ==================================================
# DNA ENCRYPTION
# ==================================================

@benchmark
def encrypt(dna_array, key_array):

    cipher_num = np.empty_like(dna_array)

    cipher_num[0] = dna_array[0] ^ key_array[0]

    for i in range(1, len(dna_array)):

        cipher_num[i] = (
            dna_array[i]
            ^ key_array[i]
            ^ cipher_num[i - 1]
        )

    return cipher_num


# ==================================================
# DNA DECRYPTION
# ==================================================

@benchmark
def decrypt(cipher_num, key_array, length):

    decrypted_num = np.empty_like(cipher_num)

    decrypted_num[0] = cipher_num[0] ^ key_array[0]

    for i in range(1, len(cipher_num)):

        decrypted_num[i] = (
            cipher_num[i]
            ^ key_array[i]
            ^ cipher_num[i - 1]
        )

    decrypted_bytes = np.empty(
        length,
        dtype=np.uint8
    )

    for i in range(length):

        decrypted_bytes[i] = reconstruct_bytes(
            decrypted_num,
            i
        )

    return decrypted_bytes


# ==================================================
# MAIN
# ==================================================

def main():

    print("Loading input file...\n")

    plaintext_bytes, file_info = load_file(INPUT_FILE)

    print(f"File Name : {file_info['name']}")
    print(f"Extension : {file_info['extension']}")
    print(f"File Size : {file_info['size_bytes']:,} bytes")
    print(f"File Size : {file_info['size_mb']:.2f} MB")

    file_size = file_info["size_bytes"]

    length = len(plaintext_bytes)

    benchmark_results = Benchmark()

    # ----------------------------------------------
    # Convert plaintext to DNA representation
    # ----------------------------------------------

    dna_array = np.empty(
        length * 4,
        dtype=np.uint8
    )

    for i, byte in enumerate(plaintext_bytes):

        dna_array[
            i * 4 : i * 4 + 4
        ] = lookup[byte]

    key_array = np.empty(
        length * 4,
        dtype=np.uint8
    )

    cipher_num = None
    decrypted_bytes = None

    # ----------------------------------------------
    # Benchmark Loop
    # ----------------------------------------------

    for run in range(NUM_RUNS):

        print(f"\nRun {run + 1}/{NUM_RUNS}")

        key_bytes = os.urandom(length)

        for i, byte in enumerate(key_bytes):

            key_array[
                i * 4 : i * 4 + 4
            ] = lookup[byte]

        # ------------------------------------------
        # Encryption
        # ------------------------------------------

        cipher_num, enc_time = encrypt(
            dna_array,
            key_array
        )

        # ------------------------------------------
        # Decryption
        # ------------------------------------------

        decrypted_bytes, dec_time = decrypt(
            cipher_num,
            key_array,
            length
        )

        # ------------------------------------------
        # Convert Ciphertext to DNA Bases
        # ------------------------------------------

        cipher_array = num_to_dna(
            cipher_num
        )

        # ------------------------------------------
        # Performance Metrics
        # ------------------------------------------

        throughput = calculate_throughput(
            file_size,
            enc_time
        )

        entropy = calculate_entropy(
            cipher_array
        )

        encryption_ratio = calculate_encryption_ratio(
            file_size,
            len(cipher_array)
        )

        # ------------------------------------------
        # Avalanche Effect
        # ------------------------------------------

        modified_plain = flip_first_bit(
            plaintext_bytes
        )

        modified_dna = np.empty(
            length * 4,
            dtype=np.uint8
        )

        for i, byte in enumerate(modified_plain):

            modified_dna[
                i * 4 : i * 4 + 4
            ] = lookup[byte]

        modified_cipher, _ = encrypt(
            modified_dna,
            key_array
        )

        avalanche = calculate_avalanche(
            cipher_num,
            modified_cipher,
            mode='symbol'
        )

        # ------------------------------------------
        # Verification
        # ------------------------------------------

        verification = verify(
            plaintext_bytes,
            decrypted_bytes
        )

        # ------------------------------------------
        # Store Benchmark Results
        # ------------------------------------------

        benchmark_results.add_run(
            enc_time,
            dec_time,
            entropy,
            throughput,
            encryption_ratio,
            avalanche,
            verification
        )

        print(
            f"Enc={enc_time:.6f}s | "
            f"Dec={dec_time:.6f}s | "
            f"TP={throughput:.2f} MB/s"
        )

    # ==================================================
    # Save Output Files
    # ==================================================

    print("\nSaving output files...")

    save_ciphertext(
        np.array(cipher_num, dtype=np.uint8).tobytes(),
        "DNA",
        ".dna"
    )

    save_decrypted_file(
        decrypted_bytes.tobytes(),
        "DNA",
        file_info["extension"]
    )

    results = benchmark_results.report()

    save_metrics(
        results,
        "DNA"
    )

    # ==================================================
    # Final Report
    # ==================================================

    benchmark_results.print_report()


# ==================================================
# PROGRAM ENTRY
# ==================================================

if __name__ == "__main__":

    main()