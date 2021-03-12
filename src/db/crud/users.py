from typing import Union

from sqlalchemy.orm import Session

from ..models import user as models


def get_one(
        db: Session,
        email: str,
) -> models.User:
    """
    Return a user object from the database
    :param db:
    :param email:
    :param get_password:
    :return:
    """
    return db.query(models.User).filter(models.User.email == email).one()


__all__ = ['get_one']
