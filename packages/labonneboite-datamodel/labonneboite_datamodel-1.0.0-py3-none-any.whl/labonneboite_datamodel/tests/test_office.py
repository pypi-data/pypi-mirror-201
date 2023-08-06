from unittest import TestCase
from .. import Office


class TestOffice(TestCase):

    def _get_valid_office(self) -> dict:
        return {
            "siret": "12346578901234",
            "naf": "1234Z",
            "company_name": "Nintendo",
            "office_name": "Mario 3",

        }

    # valid office
    def test_office_valid(self) -> None:
        data = self._get_valid_office()
        self.assertTrue(Office.validate(data).siret == "12346578901234")

    # invalid siret

    def test_siret_valid(self) -> None:
        data = self._get_valid_office()
        data["siret"] = "1".zfill(9)
        self.assertTrue(Office.validate(data).siret == "1".zfill(14))

    def test_siret_invalid(self) -> None:
        data = self._get_valid_office()
        data["siret"] = "1".zfill(8) + "abc"

        with self.assertRaises(ValueError):
            Office.validate(data)

    # invalid naf

    def test_naf_invalid(self) -> None:
        data = self._get_valid_office()

        for value in ["1".zfill(5), "0".zfill(4), "abc2".zfill(5)]:

            data["naf"] = value

            with self.assertRaises(ValueError):
                Office.validate(data)

    # phone

    def test_phone_invalid(self) -> None:
        data = self._get_valid_office()
        data["phone"] = "1".zfill(8)

        with self.assertRaises(ValueError):
            Office.validate(data)

    def test_phone_valid(self) -> None:
        data = self._get_valid_office()
        data["phone"] = "1".zfill(9)
        self.assertTrue(Office.validate(data).phone == "1".zfill(10))

    # headcount_range
    def test_headcount_range_invalid(self) -> None:
        data = self._get_valid_office()

        for value in ["1", "10-5", "00000"]:

            data["headcount_range"] = value

            self.assertTrue(Office.validate(data).headcount_range == "")

    def test_headcount_range_valid(self) -> None:
        data = self._get_valid_office()
        data["headcount_range"] = "1-2"

        self.assertTrue(Office.validate(data).headcount_range == "1-2")

    # citycode

    def test_postcode_invalid(self) -> None:
        data = self._get_valid_office()

        for value in ["1234", "abc14", "00000"]:

            data["postcode"] = value

            with self.assertRaises(ValueError):
                Office.validate(data)

    def test_postcode_valid(self) -> None:
        data = self._get_valid_office()
        data["postcode"] = "75014"
        self.assertTrue(Office.validate(data).postcode == "75014")

    # citycode
    def test_citycode_invalid(self) -> None:
        data = self._get_valid_office()

        for value in ["1234", "abc14", "00000"]:

            data["citycode"] = value

            with self.assertRaises(ValueError):
                Office.validate(data)

    def test_citycode_valid(self) -> None:
        data = self._get_valid_office()
        data["citycode"] = "75014"
        self.assertTrue(Office.validate(data).citycode == "75014")
