# Protein Variant Nomenclature Parser

This repository contains a Python library for parsing and validating colloquial protein variant nomenclature
strings like `BRAF V600E` that commonly appear in manuscripts.

## Features

- Parse protein variant nomenclature strings in the following formats:
  - Single amino acid substitution: "BRAF V600E", "BRAFV600E", "PTEN R130G", "TP53 R175H"
  - Range of amino acid substitutions: "BRAF V600_601E", "PTEN R130_131A", "TP53 R175_176N"
- Extract the components of the nomenclature string, such as gene name, prefix amino acid, position or range, and suffix amino acid
- Validate whether a given string conforms to the expected format

## Supported Nomenclature

The parser supports all HUGO gene names.

The parser supports the following amino acid single letter codes and stop codon (*).

## Installation

### From PyPI

```bash
pip install protein-variant-nomenclature-parser
```

### From Source

To install the library, clone the repository and install it using `pip`:

```bash
git clone https://github.com/yourusername/protein-variant-nomenclature-parser.git
cd protein-variant-nomenclature-parser
make install
```

### Docker container

A docker container is available:

```commandline
docker pull jeffquinnmsk/protein-variant-nomenclature-parser:latest
```

# License

This project is licensed under the MIT License. See the LICENSE file for more information.
