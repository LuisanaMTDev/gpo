import unittest
from typing import override

from opinions import format_profesor_name


class TestOpinionsFuntions(unittest.TestCase):
    @override
    def setUp(self) -> None:
        self.unformatted_professor_name = "Claridilia Ortiz Henriquez"
        self.unformatted_professor_name_with_accent_marks = "José Ramón Ynfante Ureña"

    def test_format_professor_name_without_accent_marks(self):
        formatted_professor_name = format_profesor_name(self.unformatted_professor_name)
        expected_formatted_professor_name = "claridilia-ortiz-henriquez"

        self.assertEqual(formatted_professor_name, expected_formatted_professor_name)

    def test_format_professor_name_with_accent_marks(self):
        formatted_professor_name = format_profesor_name(
            self.unformatted_professor_name_with_accent_marks
        )
        expected_formatted_professor_name = "jose-ramon-ynfante-urena"

        self.assertEqual(formatted_professor_name, expected_formatted_professor_name)


if __name__ == "__main__":
    unittest.main()
