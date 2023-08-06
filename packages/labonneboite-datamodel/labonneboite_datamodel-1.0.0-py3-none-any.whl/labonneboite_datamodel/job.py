from sqlmodel import Field
from typing import Optional
from .crud import CRUDMixin
from pydantic import validator


class Job(CRUDMixin, table=True):

    id: Optional[int] = Field(
        default=None, primary_key=True, nullable=False)

    naf: str
    rome: str
    domain: Optional[str] = Field(default=None, nullable=False)
    granddomain: Optional[str] = Field(default=None, nullable=False)

    label_granddomain: Optional[str] = Field(default=None, nullable=False)
    label_domain: Optional[str] = Field(default=None, nullable=False)
    label_naf: str
    label_rome: str

    hirings: int

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

    @validator("rome", pre=True)
    def is_rome(cls, v):
        # A valid ROME is composed 4 numbers and a letter
        error = "a ROME should be made up of 4 numbers and a letter"
        if len(v) != 5:
            raise ValueError(error)

        if not v[1:4].isdigit():
            raise ValueError(error)

        if v[0].isdigit():
            raise ValueError(error)
        return v
