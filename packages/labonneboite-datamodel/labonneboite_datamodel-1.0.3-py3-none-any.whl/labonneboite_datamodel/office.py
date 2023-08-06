from sqlmodel import Field
from typing import Optional
from .crud import CRUDMixin
from pydantic import validator
from sqlalchemy import UniqueConstraint


# validators
class OfficeCommon(CRUDMixin):
    """This is the base model applied to all Office tables

    Attributes:
        id: This is the primary key for the table
        siret: This is the company SIRET number

    """
    __table_args__ = (UniqueConstraint("siret"),)

    #: docs for baz
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)

    siret: Optional[str] = Field(
        default=None, nullable=False)

    @validator("siret", pre=True)
    def is_siret(cls, v):
        """Validator for `siret`

        Rules:
            - a SIRET should be made up of 14 numbers

        Raises:
            ValueError:


        """
        v = v.zfill(14)

        if not v.isdigit():
            raise ValueError(
                "a SIRET should be made up of 14 numbers")
        return v


class Office(OfficeCommon, table=True):
    """_summary_

    Attributes:
        naf: NAF identifier to determine in which field the company works in.
        company_name: Name of the main company.
        office_name: Name of the branch company.
        streetnumber: Street number of the company. (Optional)
        street: Street name of the company. (Optional)
        postcode: Postal code of the city where the company is, this may not be unique in France. (Optional)
        citycode: INSEE code of the city where the company is, this may is unique in France. (Optional)
        email: Email of the branch company. (Optional)
        phone: Phone of the branch company. (Optional)
        website: Website of the branch / main company. (Optional)
        headcount_range: Number of employees in the branch company. (Optional)
        flag_pmsmp:
        flag_poe_afpr:
        flag_junior:
        flag_senior:
        flag_handicap:
    """

    naf: str
    company_name: str
    office_name: str
    streetnumber: str = Field(default="", nullable=True)
    street: str = Field(default="", nullable=True)
    postcode: str = Field(default="", nullable=True)
    citycode: str = Field(default="", nullable=True)
    email: str = Field(default="", nullable=True)
    phone: str = Field(default="", nullable=True)
    website: str = Field(default="", nullable=True)

    headcount_range: str = ""

    flag_pmsmp: bool = False
    flag_poe_afpr: bool = False
    flag_junior: bool = False
    flag_senior: bool = False
    flag_handicap: bool = False

    @validator("flag_pmsmp", pre=True)
    def check_flag_pmsmp(cls, v):
        """Validator for `flag_pmsmp`

        Rules:
            - returns False if value is NULL or empty string

        """
        if isinstance(v, str) and v in ["NULL", ""]:
            return False
        return v

    @validator("flag_poe_afpr", pre=True)
    def check_flag_poe_afpr(cls, v):
        """Validator for `flag_poe_afpr`

        Rules:
            - returns False if value is NULL or empty string

        """
        if isinstance(v, str) and v in ["NULL", ""]:
            return False
        return v

    @validator("flag_junior", pre=True)
    def check_flag_junior(cls, v):
        """Validator for `flag_junior`

        Rules:
            - returns False if value is NULL or empty string

        """
        if isinstance(v, str) and v in ["NULL", ""]:
            return False
        return v

    @validator("flag_senior", pre=True)
    def check_flag_senior(cls, v):
        """Validator for `flag_senior`

        Rules:
            - returns False if value is NULL or empty string

        """
        if isinstance(v, str) and v in ["NULL", ""]:
            return False
        return v

    @validator("flag_handicap", pre=True)
    def check_flag_handicap(cls, v):
        """Validator for `flag_handicap`

        Rules:
            - returns False if value is NULL or empty string

        """

        if isinstance(v, str) and v in ["NULL", ""]:
            return False

        return v

    @validator("headcount_range", pre=True)
    def headcount_range_cleanup(cls, v):
        """Validator for `headcount_range`

        Rules:
            - the value should be a range with positive values

        """

        # the value should be a range with positive values
        values = v.split("-")

        if len(values) < 2:
            return ""

        mini = int(values[0])
        maxi = int(values[1])

        if maxi > mini:
            return f"{mini}-{maxi}"

        return ""

    @validator("phone", pre=True)
    def phone_cleanup(cls, v):
        """Validator for `phone`

        Rules:
            - Phone number is not in the expected format: either 9 or 10 numbers

        Raises:
            ValueError: Phone number is not in the expected format: either 9 or 10 numbers
        """
        if not v:
            return ""

        if len(v) < 9:
            raise ValueError(
                "Phone number is not in the expected format: either 9 or 10 numbers")
        return v.zfill(10)

    @validator("naf", pre=True)
    def is_naf(cls, v):
        """Validator for `naf`

        Rules:
            - should be 5 characters long
            - the first 4 values should be numeric
            - The last value should be a letter

        Raises:
            ValueError:

        """
        # A valid NAF is composed 4 numbers and a letter (could be a regex ^\d{4}\D{1}$)
        error = "a NAF should be made up of 4 numbers and a letter"
        if len(v) != 5:
            raise ValueError(error)

        if not v[:4].isdigit():
            raise ValueError(error)

        if v[-1].isdigit():
            raise ValueError(error)
        return v

    @validator("postcode", pre=True)
    def is_postcode(cls, v):
        """Validator for `postcode`

        Rules:
            - should be made up of at least 5 numbers
            - a postcode cannot be 00000

        Raises:
            ValueError:

        """
        if len(v) < 5:
            raise ValueError(
                "a postcode should be made up of at least 5 numbers")

        if int(v) == 0:
            raise ValueError(
                "a postcode cannot be 00000")
        return v

    @validator("citycode", pre=True)
    def is_citycode(cls, v):
        """Validator for `postcode`

        Rules:
            - should be made up of at least 5 numbers
            - a postcode should be made up of numbers
            - a postcode cannot be 00000

        Raises:
            ValueError:

        """
        if len(v) < 5:
            raise ValueError(
                "a citycode should be made up of 4 numbers and a letter")
        if not v.isdigit():
            raise ValueError(
                "a citycode should be made up of numbers")
        if int(v) == 0:
            raise ValueError(
                "a citycode cannot be 00000")
        return v


class OfficeScore(OfficeCommon, table=True):
    """This table stores the current score for each siret

    Attributes:
        score: Score provided by the ADS algorithm monthly
    """

    score: float = 0


class OfficeGps(OfficeCommon, table=True):
    """
    This is only for gps information

    Attributes:
        department_number: Department number (75, 47, etc.) where the company is.
        department: Department name where the company is.
        city:
        region:
        latitude:
        longitude:
    """

    department_number: int
    department: str
    city: str
    region: str
    latitude: float
    longitude: float
