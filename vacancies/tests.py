import pytest
from django.shortcuts import redirect

from .models import *
from django.test import TestCase
from django.urls import reverse
from django.test import Client

test_username = "test"
test_first_name = "Валерий"
test_last_name = "Альбератович"
test_password = "Ge24Grows"
test_email = "email@gmail.com"


@pytest.mark.django_db
def test_create_blog_view(new_user_verified):
    c = Client()
    response = c.post(reverse('login'), {'username': test_username, 'password': test_password})
    assert response.status_code == 302
    response = c.get(reverse('myresume'))
    assert response.status_code == 200
    response = c.get(reverse('logout'))
    assert response.status_code == 302




@pytest.mark.django_db
@pytest.mark.parametrize(['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'will_registered'],
                         [
                             (test_username, test_first_name, test_last_name, test_email, test_password, test_password,
                              True),
                             (test_username + 'a', test_first_name, test_last_name, test_email, test_password,
                              test_password, True),
                             (test_username, test_first_name, test_last_name, test_email, test_password + 'sdb',
                              test_password + 'b', False),
                             (test_username + 's', test_first_name, test_last_name, 'test' + test_email, test_password,
                              test_password, True),
                             (test_username + 'a', test_first_name, test_last_name, 'test' + test_email,
                              test_password + 'b', test_password, False),
                             (test_username, test_first_name, test_last_name, 'test' + test_email, test_password,
                              test_password, True),
                         ])
def test_register(username, first_name, last_name, email, password1, password2, will_registered):
    c = Client()
    response = c.post(reverse('register'), {'username': username,
                                            'first_name': first_name,
                                            'last_name': last_name,
                                            'password1': password1,
                                            'password2': password2,
                                            'email': email})
    if response.status_code == 302:
        assert will_registered
    else:
        assert not will_registered


@pytest.mark.django_db
@pytest.mark.parametrize(['username', 'password', 'will_logged'], [
    (test_username, test_password, True),
    (test_username + '#', test_password, False),
    (test_username, test_password + '###', False)
])
def test_login(username, password, will_logged, new_user_verified):
    c = Client()
    response = c.post(reverse('login'), {'username': username, 'password': password})
    assert will_logged == (response.status_code == 302)
