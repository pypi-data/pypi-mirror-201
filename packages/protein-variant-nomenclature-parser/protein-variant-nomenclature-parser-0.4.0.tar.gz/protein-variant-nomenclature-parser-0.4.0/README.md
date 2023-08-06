# Protein Variant Nomenclature Parser

This repository contains a Python library for parsing and validating colloquial protein variant nomenclature
strings like `BRAF V600E` that commonly appear in manuscripts.

## Features

- Parse protein variant nomenclature strings in the following formats:
  - Single amino acid substitution, e.g.: `BRAF V600E`, `BRAFV600E`, `BRAFᵛ⁶⁰⁰ᵉ`
  - Range of amino acid substitutions: `BRAFVK600_601>E`
- Extract the components of the nomenclature string, such as gene name, prefix amino acid, position or range, and suffix amino acid
- Validate whether a given string conforms to the expected format

## Usage

For parsing:

```python
from protein_variant_nomenclature_parser.parser import parse

mutation_string = "BRAF V600E"
parsed_components = parse(mutation_string)

print(parsed_components)
```

```
ProteinVariant(gene='BRAF', amino_acid_before='V', number_or_range=NumberOrRange(start=600, end=None), amino_acid_after='E')
```

For validation:

```python
from protein_variant_nomenclature_parser.parser import parse
from protein_variant_nomenclature_parser.parser import InvalidProteinVariantError


mutation_string = "INVALID V600E"

try:
    parse(mutation_string)
except InvalidProteinVariantError:
    print(f"{mutation_string} is not valid")
```

## Supported Nomenclature

The parser supports all HUGO gene names.

The parser supports the following amino acid single letter codes and stop codon (*).

The parser supports situations where the variant has no space between the gene name in the substitution,
which unfortunately comes up sometimes.

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
