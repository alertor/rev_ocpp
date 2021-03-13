from typing import Optional

from sqlalchemy.orm import Session

from ..models import user as models
from ..schemas import user as schemas


def get_one(
        db: Session,
        email: str,
) -> Optional[models.User]:
    """
    Return a user object from the database
    :param db:
    :param email:
    :param get_password:
    :return:
    """
    return db.query(models.User).filter(models.User.email == email).first()


def create(
        db: Session, *,
        user: schemas.UserCreate
) -> models.User:
    """
    Create a new user object
    :param db: Database session
    :param user: User data to use to create the new user
    :return: The new user object, or None if failed to create
    """
    new_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return user


__all__ = ['get_one']
