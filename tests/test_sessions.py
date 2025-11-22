import unittest
from io import StringIO
from typing import override

from sessions import (
    filter_sessions,
    get_professors_names,
    get_unfiltered_sessions_as_list_of_dicts,
    get_unique_days_and_hours,
)


class TestSessionsFuntions(unittest.TestCase):
    @override
    def setUp(self) -> None:
        self.sessions_file = open(
            "./excel-files/MAT-2330_2026-10.csv", "r", encoding="utf-8"
        )

        self.sessions_7030_file = open(
            "./excel-files/QUI-0140_2026-10.csv", "r", encoding="utf-8"
        )

    # TODO: Fix
    @unittest.skip("This test is broken")
    def test_filter_no_7030_sessions(self):
        filtered_sessions, is7030 = filter_sessions(
            StringIO(self.sessions_file.read()),
            days_to_exclude=["SA"],
            hours_to_exclude=["19 a 22", "20 a 22"],
        )
        expected_filtered_sessions = [
            {
                "NRC": 27342,
                "Sec": "ZC1",
                "Tipo": "Teoria",
                "Campus": "Santo Domingo",
                "Horario": "13 a 15",
                "Días": "LU",
                "Edificios": "Ciencias Juridicas A",
                "Aula": "CJA-104",
                "Modalidad": "Semipresencial",
                "Cupos": 60,
                "Inscritos": 0,
                "Disponibles": 60,
                "Profesor(a)": "Elpidio Antonio Perez Vargas",
            },
            {
                "NRC": 41799,
                "Sec": "20",
                "Tipo": "Teoria",
                "Campus": "Santo Domingo",
                "Horario": "15 a 18",
                "Días": "JUVI",
                "Edificios": "Liceo Hugo Tolentino Dipp Edi3",
                "Aula": "HTD3-204",
                "Modalidad": "Presencial",
                "Cupos": 60,
                "Inscritos": 0,
                "Disponibles": 60,
                "Profesor(a)": "Marc Kelly Jean Philippe",
            },
        ]
        expected_is7030 = False
        self.assertEqual(filtered_sessions, expected_filtered_sessions)
        self.assertEqual(is7030, expected_is7030)

    # TODO: Fix
    @unittest.skip("This test is broken")
    def test_filter_7030_sessions(self):
        filtered_sessions, is7030 = filter_sessions(
            StringIO(self.sessions_7030_file.read()),
            days_to_exclude=["SA"],
            hours_to_exclude=["19 a 22", "20 a 22"],
        )
        expected_filtered_sessions = [
            {
                "NRC": 47321,
                "Sec": "Y02",
                "Tipo": "Laboratorio",
                "Campus": "Yamasá",
                "Horario": "16 a 19",
                "Días": "MI",
                "Edificios": "Extension Yamasa",
                "Aula": "YAM-102",
                "Modalidad": "Presencial",
                "Cupos": 25,
                "Inscritos": 0,
                "Disponibles": 25,
                "Profesor(a)": "Cristina Laurencio Jimenez",
            }
        ]
        expected_is7030 = True
        self.assertEqual(filtered_sessions, expected_filtered_sessions)
        self.assertEqual(is7030, expected_is7030)

    # TODO: Fix
    @unittest.skip("This test is broken")
    def test_get_unfiltered_sessions(self):
        unfiltered_sessions = get_unfiltered_sessions_as_list_of_dicts(
            StringIO(self.sessions_7030_file.read())
        )
        expected_unfiltered_sessions = [
            {
                "NRC": 47320,
                "Sec": "Y01",
                "Tipo": "Teoria",
                "Campus": "Yamasá",
                "Horario": "10 a 12",
                "Días": "MI",
                "Edificios": "Extension Yamasa",
                "Aula": "YAM-101",
                "Modalidad": "Presencial",
                "Cupos": 50,
                "Inscritos": 0,
                "Disponibles": 50,
                "Profesor(a)": "Cristina Laurencio Jimenez",
            },
            {
                "NRC": 47321,
                "Sec": "Y02",
                "Tipo": "Laboratorio",
                "Campus": "Yamasá",
                "Horario": "16 a 19",
                "Días": "MI",
                "Edificios": "Extension Yamasa",
                "Aula": "YAM-102",
                "Modalidad": "Presencial",
                "Cupos": 25,
                "Inscritos": 0,
                "Disponibles": 25,
                "Profesor(a)": "Cristina Laurencio Jimenez",
            },
            {
                "NRC": 47322,
                "Sec": "Y03",
                "Tipo": "Laboratorio",
                "Campus": "Yamasá",
                "Horario": "13 a 16",
                "Días": "SA",
                "Edificios": "Extension Yamasa",
                "Aula": "YAM-103",
                "Modalidad": "Presencial",
                "Cupos": 25,
                "Inscritos": 0,
                "Disponibles": 25,
                "Profesor(a)": "Cristina Laurencio Jimenez",
            },
        ]

        self.assertEqual(unfiltered_sessions, expected_unfiltered_sessions)

    def test_get_unique_days_and_hours(self):
        days, hours = get_unique_days_and_hours(StringIO(self.sessions_file.read()))
        expected_days = ["VI", "SA", "LU", "MI", "JUVI", "MA"]
        expected_hours = ["13 a 16", "19 a 22", "15 a 18", "20 a 22", "13 a 15"]

        self.assertEqual(days, expected_days)
        self.assertEqual(hours, expected_hours)

    def test_get_professors_names(self):
        professors_names = get_professors_names(StringIO(self.sessions_file.read()))
        expected_profesors_names = [
            "Cristino Castillo Marte",
            "Marc Kelly Jean Philippe",
            "Eric Tomas Beriguete Galan",
            "Elpidio Antonio Perez Vargas",
        ]
        self.assertEqual(professors_names, expected_profesors_names)

    @override
    def tearDown(self) -> None:
        self.sessions_file.close()
        self.sessions_7030_file.close()


if __name__ == "__main__":
    unittest.main()
