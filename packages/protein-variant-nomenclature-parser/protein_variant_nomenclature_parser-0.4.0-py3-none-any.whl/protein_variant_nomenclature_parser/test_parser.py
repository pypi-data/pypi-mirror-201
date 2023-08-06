import unittest
from protein_variant_nomenclature_parser.parser import (
    InvalidProteinVariantError,
    parse,
    ProteinVariant,
    NumberOrRange,
)


class TestParser(unittest.TestCase):
    def test_simple_mutation_with_space(self):
        input_string = "ZSWIM9 V600E"
        expected_output = ProteinVariant("ZSWIM9", "V", NumberOrRange(600), "E")
        self.assertEqual(parse(input_string), expected_output)

    def test_simple_mutation_no_space(self):
        input_string = "BRAFV600E"
        expected_output = ProteinVariant("BRAF", "V", NumberOrRange(600), "E")
        self.assertEqual(parse(input_string), expected_output)

    def test_ambiguous_hugo_prefix(self):
        # This is an ambiguous one if there's not any whitespace, we should
        # handle this in the future
        input_string = "CGA SS600E"
        expected_output = ProteinVariant("CGA", "SS", NumberOrRange(600), "E")
        self.assertEqual(parse(input_string), expected_output)

        input_string = "CGASS600E"
        expected_output = ProteinVariant("CGAS", "S", NumberOrRange(600), "E")
        self.assertEqual(parse(input_string), expected_output)

    def test_simple_mutation_superscript(self):
        input_string = "BRAFᵛ⁶⁰⁰ᵉ"
        expected_output = ProteinVariant("BRAF", "V", NumberOrRange(600), "E")
        self.assertEqual(parse(input_string), expected_output)

    def test_range_mutation(self):
        input_string = "BRAFVK600_601>E"
        expected_output = ProteinVariant("BRAF", "VK", NumberOrRange(600, 601), "E")

        self.assertEqual(parse(input_string), expected_output)

    def test_invalid_mutation(self):
        input_string = "INVALID V600E"
        with self.assertRaises(InvalidProteinVariantError):
            parse(input_string)

    def test_invalid_amino_acid(self):
        input_string = "BRAF X600E"
        with self.assertRaises(InvalidProteinVariantError):
            parse(input_string)

    def test_invalid_position(self):
        input_string = "BRAF V600.5E"
        with self.assertRaises(InvalidProteinVariantError):
            parse(input_string)


if __name__ == "__main__":
    unittest.main()
