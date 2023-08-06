from sqlmodel import Field, SQLModel, text

from datetime import datetime


class CRUDMixin(SQLModel):
    """This table provides the base elements for all tables in database

    Attributes:
        date_created:
        last_modified: This field should automatically update when the line is updated
    """
    date_created: datetime = Field(
        default_factory=datetime.utcnow, nullable=False)

    # https://docs.sqlalchemy.org/en/20/dialects/mysql.html#mysql-timestamp-onupdate
    last_modified: datetime = Field(
        default_factory=datetime.utcnow, nullable=False, sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
        },)
