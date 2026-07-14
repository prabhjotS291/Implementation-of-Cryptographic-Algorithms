import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

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
# AES-256 ENCRYPTION
# ==================================================

@benchmark
def encrypt(plaintext_bytes, key, iv):

    cipher = AES.new(
        key,
        AES.MODE_CBC,
        iv
    )

    padded_data = pad(
        plaintext_bytes,
        AES.block_size
    )

    ciphertext = cipher.encrypt(
        padded_data
    )

    return ciphertext


# ==================================================
# AES-256 DECRYPTION
# ==================================================

@benchmark
def decrypt(ciphertext, key, iv):

    cipher = AES.new(
        key,
        AES.MODE_CBC,
        iv
    )

    decrypted_padded = cipher.decrypt(
        ciphertext
    )

    plaintext = unpad(
        decrypted_padded,
        AES.block_size
    )

    return plaintext


# ==================================================
# MAIN
# ==================================================

def main():

    # ----------------------------------------------
    # Load Input File
    # ----------------------------------------------

    print("Loading input file...\n")

    plaintext_bytes, file_info = load_file(INPUT_FILE)

    print(f"File Name : {file_info['name']}")
    print(f"Extension : {file_info['extension']}")
    print(f"File Size : {file_info['size_bytes']:,} bytes")
    print(f"File Size : {file_info['size_mb']:.2f} MB")

    file_size = file_info["size_bytes"]

    benchmark_results = Benchmark()

    ciphertext = None
    decrypted_data = None

    # ----------------------------------------------
    # Benchmark Loop
    # ----------------------------------------------

    for run in range(NUM_RUNS):

        print(f"\nRun {run + 1}/{NUM_RUNS}")

        # ------------------------------------------
        # Key Generation
        # ------------------------------------------

        key = os.urandom(32)

        iv = os.urandom(16)

        # ------------------------------------------
        # Encryption
        # ------------------------------------------

        ciphertext, enc_time = encrypt(
            plaintext_bytes.tobytes(),
            key,
            iv
        )

        # ------------------------------------------
        # Decryption
        # ------------------------------------------

        decrypted_data, dec_time = decrypt(
            ciphertext,
            key,
            iv
        )

        # ------------------------------------------
        # Performance Metrics
        # ------------------------------------------

        throughput = calculate_throughput(
            file_size,
            enc_time
        )

        entropy = calculate_entropy(
            ciphertext
        )

        encryption_ratio = calculate_encryption_ratio(
            file_size,
            len(ciphertext)
        )

        # ------------------------------------------
        # Avalanche Effect
        # ------------------------------------------

        modified_plaintext = flip_first_bit(
            plaintext_bytes
        )

        modified_ciphertext, _ = encrypt(
            bytes(modified_plaintext),
            key,
            iv
        )

        avalanche = calculate_avalanche(
            ciphertext,
            modified_ciphertext
        )

        # ------------------------------------------
        # Verification
        # ------------------------------------------

        verification = verify(
            plaintext_bytes,
            decrypted_data
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

    # --------------------------------------------------
    # Save Output Files
    # --------------------------------------------------

    print("\nSaving output files...")

    save_ciphertext(
        ciphertext,
        "AES",
        ".aes"
    )

    save_decrypted_file(
        decrypted_data,
        "AES",
        file_info["extension"]
    )

    results = benchmark_results.report()

    save_metrics(
        results,
        "AES"
    )

    # --------------------------------------------------
    # Final Report
    # --------------------------------------------------

    benchmark_results.print_report()


# ==================================================
# PROGRAM ENTRY
# ==================================================

if __name__ == "__main__":

    main()