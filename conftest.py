import pytest
from vacancies.models import *

test_username = "test"
test_first_name = "Валерий"
test_last_name = "Альбератович"
test_password = "Ge24Grows"
test_email = "email@gmail.com"


@pytest.fixture
def new_user_verified():
    user_verified = User.objects.create_user(username=test_username,
                                             password=test_password,
                                             email=test_email)
    resume_verified = Resume.objects.create(user=user_verified, verified=True)
    yield user_verified
    resume_verified.delete()
    user_verified.delete()
