import math
import statistics
from collections import Counter
import numpy as np

# ==================================================
# ENTROPY
# ==================================================

def calculate_entropy(data):
    """
    Calculates Shannon entropy of the ciphertext.

    Parameters:
        data (bytes | bytearray | numpy.ndarray)

    Returns:
        float
    """

    if isinstance(data, np.ndarray):
        data = data.tobytes()

    counts = Counter(data)
    total = len(data)

    entropy = 0.0

    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)

    return entropy


# ==================================================
# FLIP FIRST BIT
# ==================================================

def flip_first_bit(data):
    """
    Flips the least significant bit of the first byte.

    This deterministic implementation is used to ensure
    consistent avalanche effect measurements across all
    cryptographic algorithms.
    """

    if isinstance(data, np.ndarray):
        data = data.copy()
    else:
        data = bytearray(data)

    data[0] ^= 0x01

    return data


# ==================================================
# AVALANCHE EFFECT
# ==================================================

# def calculate_avalanche(ciphertext1, ciphertext2):
#     """
#     Calculates avalanche effect between two ciphertexts.

#     Parameters:
#         ciphertext1
#         ciphertext2

#     Returns:
#         float (percentage)
#     """

#     if isinstance(ciphertext1, np.ndarray):
#         ciphertext1 = ciphertext1.tobytes()

#     if isinstance(ciphertext2, np.ndarray):
#         ciphertext2 = ciphertext2.tobytes()

#     changed_bits = 0

#     total_bits = min(
#         len(ciphertext1),
#         len(ciphertext2)
#     ) * 8

#     for b1, b2 in zip(ciphertext1, ciphertext2):
#         xor = b1 ^ b2
#         changed_bits += xor.bit_count()

#     return (changed_bits / total_bits) * 100

def calculate_avalanche(ciphertext1, ciphertext2, mode="bit"):

    if mode == "symbol":

        if not isinstance(ciphertext1, np.ndarray):
            ciphertext1 = np.frombuffer(ciphertext1, dtype=np.uint8)

        if not isinstance(ciphertext2, np.ndarray):
            ciphertext2 = np.frombuffer(ciphertext2, dtype=np.uint8)

        changed = np.sum(ciphertext1 != ciphertext2)

        return (changed / len(ciphertext1)) * 100

    # -------- Bit mode --------

    if isinstance(ciphertext1, np.ndarray):
        ciphertext1 = ciphertext1.tobytes()

    if isinstance(ciphertext2, np.ndarray):
        ciphertext2 = ciphertext2.tobytes()

    changed_bits = 0

    total_bits = min(
        len(ciphertext1),
        len(ciphertext2)
    ) * 8

    for b1, b2 in zip(ciphertext1, ciphertext2):

        changed_bits += (b1 ^ b2).bit_count()

    return (changed_bits / total_bits) * 100


# ==================================================
# THROUGHPUT
# ==================================================

def calculate_throughput(file_size_bytes, encryption_time):

    return (
        file_size_bytes /
        encryption_time /
        (1024 * 1024)
    )


# ==================================================
# ENCRYPTION RATIO
# ==================================================

def calculate_encryption_ratio(plaintext_size, ciphertext_size):

    return ciphertext_size / plaintext_size


# ==================================================
# VERIFICATION
# ==================================================

def verify(original, decrypted):

    if isinstance(original, np.ndarray):
        original = original.tobytes()

    if isinstance(decrypted, np.ndarray):
        decrypted = decrypted.tobytes()

    return original == decrypted
