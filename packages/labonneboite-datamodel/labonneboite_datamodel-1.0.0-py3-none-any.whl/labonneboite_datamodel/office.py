from sqlmodel import Field
from typing import Optional
from .crud import CRUDMixin
from pydantic import validator
from sqlalchemy import UniqueConstraint


# validators
class OfficeCommon(CRUDMixin):
    __table_args__ = (UniqueConstraint("siret"),)
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)

    siret: Optional[str] = Field(
        default=None, nullable=False)

    @validator("siret", pre=True)
    def is_siret(cls, v):
        # A valid SIRET is composed of 14 digits
        v = v.zfill(14)

        if not v.isdigit():
            raise ValueError(
                "a SIRET should be made up of 14 numbers")
        return v


class Office(OfficeCommon, table=True):
    """
    This should be the core data provided by ADS
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

    @validator("headcount_range", pre=True)
    def headcount_range_cleanup(cls, v):

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

        if len(v) < 9:
            raise ValueError(
                "Phone number is not in the expected format: either 9 or 10 numbers")
        return v.zfill(10)

    @validator("naf", pre=True)
    def is_naf(cls, v):
        # A valid NAF is composed 4 numbers and a letter
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

        if len(v) < 5:
            raise ValueError(
                "a postcode should be made up of at least 5 numbers")
        if not v.isdigit():
            raise ValueError(
                "a postcode should be made up of numbers")
        if int(v) == 0:
            raise ValueError(
                "a postcode cannot be 00000")
        return v

    @validator("citycode", pre=True)
    def is_citycode(cls, v):

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
    """
    This should be the core data provided by ADS
    """

    score: float = 0


class OfficeGps(OfficeCommon, table=True):
    """
    This is only for gps information
    """

    department_number: int
    department: str
    city: str
    region: str
    latitude: float
    longitude: float
