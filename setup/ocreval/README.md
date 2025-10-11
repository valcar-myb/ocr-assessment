# ocreval - ISRI Analytic Tools for OCR Evaluation

This project uses [ocreval](https://github.com/eddieantonio/ocreval) for accurate OCR evaluation metrics, particularly for character and word accuracy calculations.

`ocreval` is a modern port of the ISRI Analytic Tools for OCR Evaluation with UTF-8 support and consists of 17 tools for measuring OCR performance.

## About ocreval

**Repository**: https://github.com/eddieantonio/ocreval  
**License**: Apache-2.0  
**Features**:
- UTF-8 support for multilingual OCR evaluation
- 17 specialized tools for OCR performance measurement
- Industry-standard metrics (Character Error Rate, Word Error Rate, etc.)
- Based on ISRI Analytic Tools used in OCR research

## Installation

### macOS

Using Homebrew:

```bash
brew install eddieantonio/eddieantonio/ocreval
```

### Ubuntu/Debian

#### 1. Install build dependencies

```bash
sudo apt install build-essential libutf8proc-dev
```

If `libutf8proc-dev` is not available via apt, install it manually:

```bash
curl -OL https://github.com/JuliaStrings/utf8proc/archive/v1.3.1.tar.gz
tar xzf v1.3.1.tar.gz
cd utf8proc-1.3.1/
make
sudo make install
sudo ldconfig
cd -
```

#### 2. Build and install ocreval

```bash
# Clone the repository
git clone https://github.com/eddieantonio/ocreval.git
cd ocreval

# Build
make

# Install to /usr/local/
sudo make install

# Or install "locally" (adds to PATH without copying files)
make exports >> ~/.bashrc
source ~/.bashrc
```

### Verify Installation

Check that the tools are installed correctly:

```bash
# Check if accuracy tool is available
which accuracy

# Test with version/help
accuracy -h
```

## Available Tools

ocreval provides 17 tools for OCR evaluation:

1. **accuracy** - Calculate character and word accuracy
2. **wordacc** - Word-level accuracy
3. **editop** - Edit operations analysis
4. **accsum** - Accuracy summary
5. **groupacc** - Group accuracy statistics
6. **wordfreq** - Word frequency analysis
7. **ngram** - N-gram analysis
8. And more...

For this project, we primarily use:
- **accuracy**: For character and word accuracy metrics
- **wordacc**: For detailed word-level analysis

## Usage in This Project

The `ocreval` tools are integrated into our accuracy evaluation module at `src/evaluation/accuracy/`.

See `src/evaluation/accuracy/README.md` for details on how the tools are used in the evaluation pipeline.

## Citation

If you use this tool in your research, please cite:

```bibtex
@inproceedings{santos-2019-ocr,
    title = "{OCR} evaluation tools for the 21st century",
    author = "Santos, Eddie Antonio",
    booktitle = "Proceedings of the 3rd Workshop on the Use of Computational Methods in the Study of Endangered Languages Volume 1 (Papers)",
    month = feb,
    year = "2019",
    address = "Honolulu",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W19-6004",
    pages = "23--27",
}
```

**Paper**: https://www.aclweb.org/anthology/W19-6004/

## Original Credits

### ocreval
- Copyright 2015–2017 Eddie Antonio Santos
- Copyright © 2018–2021 National Research Council Canada

### The ISRI Analytic Tools for OCR Evaluation
- Copyright 1996 The Board of Regents of the Nevada System of Higher Education, on behalf of the University of Nevada, Las Vegas, Information Science Research Institute

## License

Licensed under the Apache License, Version 2.0.


### UTF-8 encoding issues

Ensure your text files are UTF-8 encoded. **ocreval requires UTF-8 encoding.**

#### Check encoding:

```bash
# Check a single file
file -i your_file.txt
# Should show: text/plain; charset=utf-8
```

#### Verify all text files in the project:

```bash
# Check if all text files are UTF-8
python experiments/verify_utf8.py

# Check and convert non-UTF-8 files automatically
python experiments/verify_utf8.py --convert

# Also check ground truth files
python experiments/verify_utf8.py --check-ground-truth --convert
```

#### Manual conversion:

```bash
# Convert a single file
iconv -f ISO-8859-1 -t UTF-8 input.txt > output.txt

# Or with Python
python3 -c "data=open('input.txt','r',encoding='latin-1').read(); open('output.txt','w',encoding='utf-8').write(data)"
```

## Additional Resources

- [ocreval Documentation](https://eddieantonio.ca/ocreval/)
- [Original ISRI Tools (archived)](https://code.google.com/archive/p/isri-ocr-evaluation-tools/)
- [User Guide PDF](https://github.com/eddieantonio/ocreval/blob/master/user-guide.pdf)

