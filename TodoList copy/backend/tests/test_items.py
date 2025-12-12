# test_crud.py
from app.models import User, Item
from app.crud import create_user, get_user_by_email
import pytest
import uuid


def test_create_user(session):

    # Create a user
    user = create_user(session, "alice@example.com")

    # Test that the user was inserted
    fetched = get_user_by_email(session, "alice@example.com")
    assert fetched is not None
    assert fetched.email == "alice@example2.com"
    # assert fetched.hashed_password == "hashedpassword"


def test_email_required(session):
    # Email is required
    with pytest.raises(Exception):
        user = User(id=uuid.uuid4(), hashed_password="pass")  # missing email
        session.add(user)
        session.commit()


def test_user_defaults(session):
    # `is_active` and `is_superuser` have defaults
    user = User(id=uuid.uuid4(), email="carol@example.com", hashed_password="pass")
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.is_active is True
    assert user.is_superuser is False


# test_relationships.py
def test_user_item_relationship(session):
    user = User(id=uuid.uuid4(), email="bob@example.com", hashed_password="pass")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Add items for this user
    item1 = Item(title="Item 1", owner_id=user.id)
    item2 = Item(title="Item 2", owner_id=user.id)
    session.add_all([item1, item2])
    session.commit()
    session.refresh(user)

    # Test that relationship works
    assert len(user.items) == 2
    titles = [item.title for item in user.items]
    assert "Item 1" in titles and "Item 2" in titles
