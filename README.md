# 🔐 Implementation of Cryptographic Algorithms

A modular Python implementation and performance benchmarking framework for comparing multiple cryptographic algorithms.

This project implements and evaluates the following encryption algorithms:

- AES-256 (Advanced Encryption Standard)
- DES (Data Encryption Standard)
- DNA-Based Encryption
- Logistic Map Based Chaotic Encryption

The project was developed as part of a cryptography research internship and focuses on comparing the performance and security characteristics of different encryption techniques.

---

## Features

- Modular implementation of all algorithms
- Common benchmarking framework
- Automatic performance evaluation
- Entropy calculation
- Avalanche effect analysis
- Throughput calculation
- Encryption ratio calculation
- Encryption/Decryption verification
- File-based encryption support

---

## Project Structure

```
Implementation-of-Cryptographic-Algorithms/
│
├── AES.py
├── DES.py
├── DNA.py
├── ChaoticMap.py
│
├── input/
│   └── image.png
│
├── output/
│
├── utils/
│   ├── benchmark.py
│   ├── file_handler.py
│   ├── metrics.py
│   └── save_files.py
│
├── .gitignore
└── README.md
```

---

## Algorithms Implemented

### AES-256

- AES-256 in CBC mode
- 256-bit symmetric key
- PKCS#7 padding
- Random IV generation

---

### DES

- DES in CBC mode
- 56-bit symmetric key
- PKCS#7 padding
- Random IV generation

---

### DNA-Based Encryption

- DNA encoding using lookup table
- DNA XOR operations
- Chained diffusion mechanism
- DNA decoding

---

### Chaotic Map Encryption

- Logistic Map based chaotic sequence generation
- Permutation stage
- XOR diffusion
- Feedback diffusion

---

## Evaluation Metrics

The implementations are evaluated using the following metrics:

- Encryption Time
- Decryption Time
- Throughput (MB/s)
- Information Entropy
- Avalanche Effect
- Encryption Ratio
- Verification Accuracy

---

## Requirements

- Python 3.14+
- NumPy
- PyCryptodome

Install dependencies:

```bash
pip install numpy pycryptodome
```

---

## Running the Project

Place the input image inside the `input` directory.

Run any implementation individually:

```bash
python AES.py
```

```bash
python DES.py
```

```bash
python DNA.py
```

```bash
python ChaoticMap.py
```

Generated outputs are stored in the `output` directory.

---

## Current Status

✔ AES Implementation

✔ DES Implementation

✔ DNA Encryption Implementation

✔ Chaotic Map Encryption Implementation

✔ Modular Utility Framework

✔ Benchmarking Framework

---

## Dataset

The encryption algorithms in this project are evaluated using a PNG image located in the `input` directory.

**Image Source:**
https://example.com/your-image-link

The same image is used as the input for all encryption algorithms to ensure a fair and consistent comparison of their performance and security metrics.

---

## Future Improvements

- Improve diffusion stage of the chaotic map algorithm
- Support additional file formats
- Add more cryptographic algorithms
- Performance optimization

---

## Author

**Prabhjot Singh**

B.Tech Computer Science Engineering (AI & ML)

---

## License

This project is intended for educational and research purposes.