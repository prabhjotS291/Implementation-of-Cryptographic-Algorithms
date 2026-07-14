import time
import statistics
from functools import wraps

# ==================================================
# FUNCTION TIMER DECORATOR
# ==================================================

def benchmark(func):
    """
    Decorator that measures the execution time of
    any function.

    Returns
        result, elapsed_time
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        start = time.perf_counter()

        result = func(*args, **kwargs)

        end = time.perf_counter()

        elapsed_time = end - start

        return result, elapsed_time

    return wrapper


# ==================================================
# BENCHMARK CLASS
# ==================================================

class Benchmark:

    def __init__(self):

        self.encryption_times = []
        self.decryption_times = []

        self.entropies = []
        self.avalanches = []

        self.throughputs = []
        self.encryption_ratios = []

        self.verifications = []


    # ==================================================
    # ADD A SINGLE RUN
    # ==================================================

    def add_run(
        self,
        enc_time,
        dec_time,
        entropy,
        throughput,
        encryption_ratio,
        avalanche,
        verification
    ):

        self.encryption_times.append(enc_time)
        self.decryption_times.append(dec_time)

        self.entropies.append(entropy)
        self.throughputs.append(throughput)
        self.encryption_ratios.append(encryption_ratio)

        self.avalanches.append(avalanche)

        self.verifications.append(verification)


    # ==================================================
    # PRIVATE HELPER FUNCTIONS
    # ==================================================

    def _average(self, values):

        return statistics.mean(values)


    def _std_dev(self, values):

        if len(values) <= 1:
            return 0.0

        return statistics.stdev(values)


    # ==================================================
    # TOTAL NUMBER OF RUNS
    # ==================================================

    def total_runs(self):

        return len(self.encryption_times)


    # ==================================================
    # GENERATE REPORT
    # ==================================================

    def report(self):

        return {

            "runs": self.total_runs(),

            "avg_enc": self._average(self.encryption_times),
            "std_enc": self._std_dev(self.encryption_times),

            "avg_dec": self._average(self.decryption_times),
            "std_dec": self._std_dev(self.decryption_times),

            "avg_tp": self._average(self.throughputs),
            "std_tp": self._std_dev(self.throughputs),

            "avg_entropy": self._average(self.entropies),

            "avg_ratio": self._average(self.encryption_ratios),

            "avg_avalanche": self._average(self.avalanches),

            "verification": all(self.verifications)

        }


    # ==================================================
    # PRINT REPORT
    # ==================================================

    def print_report(self):

        results = self.report()

        print("\n")
        print("=" * 60)
        print("FINAL BENCHMARK REPORT")
        print("=" * 60)

        print(f"Total Runs              : {results['runs']}")

        print()

        print(f"Average Encryption Time : {results['avg_enc']:.8f} sec")
        print(f"Encryption Std Dev      : {results['std_enc']:.8f}")

        print()

        print(f"Average Decryption Time : {results['avg_dec']:.8f} sec")
        print(f"Decryption Std Dev      : {results['std_dec']:.8f}")

        print()

        print(f"Average Throughput      : {results['avg_tp']:.4f} MB/s")
        print(f"Throughput Std Dev      : {results['std_tp']:.4f}")

        print()

        print(f"Average Entropy         : {results['avg_entropy']:.8f}")

        print(f"Average Encryption Ratio: {results['avg_ratio']:.6f}")

        print(f"Average Avalanche       : {results['avg_avalanche']:.4f}%")

        print()

        print(f"Verification            : {results['verification']}")

        print("=" * 60)


    # ==================================================
    # CLEAR ALL STORED RESULTS
    # ==================================================

    def clear(self):

        self.encryption_times.clear()
        self.decryption_times.clear()

        self.entropies.clear()
        self.throughputs.clear()
        self.encryption_ratios.clear()

        self.avalanches.clear()

        self.verifications.clear()