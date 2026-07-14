import os
import random
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
# LOGISTIC MAP
# ==================================================

def logisticMap(length, x0, r):

    sequence = np.empty(length, dtype=np.float64)

    x = x0

    for i in range(length):

        x = r * x * (1 - x)

        sequence[i] = x

    return sequence


# ==================================================
# PERMUTATION
# ==================================================

def getPermutationIndices(length, x0, r):

    chaos_seq = logisticMap(
        length,
        x0,
        r
    )

    return np.argsort(chaos_seq)


def getInversePermutation(perm_idx):

    inv_perm = np.empty_like(
        perm_idx
    )

    inv_perm[perm_idx] = np.arange(
        len(perm_idx)
    )

    return inv_perm


# ==================================================
# KEYSTREAM
# ==================================================

def getChaoticKeystream(length, x0, r):

    chaos_seq = logisticMap(
        length,
        x0,
        r
    )

    return np.floor(
        chaos_seq * 256
    ).astype(np.uint8)


# ==================================================
# ENCRYPTION
# ==================================================


def _encrypt_core(
    plaintext_bytes,
    length,
    parameters
):

    # Permutation

    perm_idx = getPermutationIndices(
        length,
        parameters[0],
        parameters[2]
    )

    permuted_plaintext = plaintext_bytes[
        perm_idx
    ]

    # Diffusion

    keystream = getChaoticKeystream(
        length,
        parameters[1],
        parameters[2]
    )

    ciphertext = np.empty(
        length,
        dtype=np.uint8
    )

    ciphertext[0] = (
        permuted_plaintext[0]
        ^ keystream[0]
    )

    for i in range(1, length):

        feedback = (
            int(ciphertext[i - 1])
            + int(permuted_plaintext[i - 1])
        ) % 256

        ciphertext[i] = (
            permuted_plaintext[i]
            ^ keystream[i]
            ^ feedback
        )

    return ciphertext

@benchmark
def encrypt(
    plaintext_bytes,
    length,
    parameters
):
    return _encrypt_core(plaintext_bytes, length, parameters)


# ==================================================
# DECRYPTION
# ==================================================

@benchmark
def decrypt(
    ciphertext,
    length,
    parameters
):

    keystream = getChaoticKeystream(
        length,
        parameters[1],
        parameters[2]
    )

    permuted_plaintext = np.empty(
        length,
        dtype=np.uint8
    )

    permuted_plaintext[0] = (
        ciphertext[0]
        ^ keystream[0]
    )

    for i in range(1, length):

        feedback = (
            int(ciphertext[i - 1])
            + int(permuted_plaintext[i - 1])
        ) % 256

        permuted_plaintext[i] = (
            ciphertext[i]
            ^ keystream[i]
            ^ feedback
        )

    perm_idx = getPermutationIndices(
        length,
        parameters[0],
        parameters[2]
    )

    inv_perm = getInversePermutation(
        perm_idx
    )

    decrypted_plaintext = permuted_plaintext[
        inv_perm
    ]

    return decrypted_plaintext


# ==================================================
# MAIN
# ==================================================

def main():

    print("Loading input file...\n")

    plaintext_bytes, file_info = load_file(
        INPUT_FILE
    )

    print(f"File Name : {file_info['name']}")
    print(f"Extension : {file_info['extension']}")
    print(f"File Size : {file_info['size_bytes']:,} bytes")
    print(f"File Size : {file_info['size_mb']:.2f} MB")

    length = len(plaintext_bytes)

    file_size = file_info["size_bytes"]

    benchmark_results = Benchmark()

    ciphertext = None
    decrypted_data = None

    # ------------------------------------------
    # Benchmark Loop
    # ------------------------------------------

    for run in range(NUM_RUNS):

        print(f"\nRun {run + 1}/{NUM_RUNS}")

        parameters = (
            random.uniform(0.1, 0.9),
            random.uniform(0.1, 0.9),
            3.99
        )

        ciphertext, enc_time = encrypt(
            plaintext_bytes,
            length,
            parameters
        )

        decrypted_data, dec_time = decrypt(
            ciphertext,
            length,
            parameters
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

        avalanche_values = []

        for _ in range(5):

            modified_plaintext = plaintext_bytes.copy()

            byte_index = random.randint(
                0,
                length - 1
            )

            bit_position = random.randint(
                0,
                7
            )

            modified_plaintext[byte_index] ^= (
                1 << bit_position
            )

            modified_ciphertext = _encrypt_core(
                modified_plaintext,
                length,
                parameters
            )

            avalanche_values.append(

                calculate_avalanche(
                    ciphertext,
                    modified_ciphertext,
                    mode="bit"
                )

            )

        avalanche = sum(avalanche_values) / len(avalanche_values)

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

    # ==================================================
    # Save Output Files
    # ==================================================

    print("\nSaving output files...")

    save_ciphertext(
        ciphertext.tobytes(),
        "Chaotic_Map",
        ".chaos"
    )

    save_decrypted_file(
        decrypted_data.tobytes(),
        "Chaotic_Map",
        file_info["extension"]
    )

    results = benchmark_results.report()

    save_metrics(
        results,
        "Chaotic_Map"
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