from unittest import TestCase
from .. import Job


class TestOffice(TestCase):

    def _get_valid_job(self) -> dict:
        return {
            "rome": "M1234",
            "naf": "1234Z",
            "label_naf": "Something",
            "label_rome": "Something",
            "hirings": 60

        }

    # valid job
    def test_job_valid(self) -> None:
        data = self._get_valid_job()
        self.assertTrue(Job.validate(data).rome == "M1234")

    # invalid naf

    def test_naf_invalid(self) -> None:
        data = self._get_valid_job()

        for value in ["1".zfill(5), "0".zfill(4), "abc2".zfill(5)]:

            data["naf"] = value

            with self.assertRaises(ValueError):
                Job.validate(data)

    # invalid naf

    def test_rome_invalid(self) -> None:
        data = self._get_valid_job()

        for value in ["1".zfill(5), "0".zfill(4), "abc2".zfill(5)]:

            data["rome"] = value

            with self.assertRaises(ValueError):
                Job.validate(data)
