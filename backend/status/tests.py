import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, CoreAPIClient

User = get_user_model()


def test_smoke():
    # Is Pytest working?
    assert True

    # Check if Django admin login page is reachable
    client = APIClient()
    response = client.get('/admin/login/')

    assert response.status_code == 200
    assert response.context_data.get('title') == 'Log in'


def test_docs():
    # Docs page is reachable
    client = APIClient()
    response = client.get('/api/docs/')

    assert response.status_code == 200
    assert response.data.title == 'API Docs'


# TODO: Coreapi tests are not yet working because of the schema issue, uncomment when fixed
# @pytest.mark.django_db
# def test_coreapi():
#     test_user = User(username='test', password='test')
#     test_user.save()
#
#     # Docs page can return coreapi schema if requested
#
#     client = CoreAPIClient()
#     # TODO: Find a way to get schema json from backend, this seems to return html...
#     schema = client.get('http://localhost:8000/api/docs/')
#
#     # Create a new organisation
#     action = ["auth", "login", "create"]
#     params = {
#         "username": 'test',
#         "password": "test",
#     }
#
#     # TODO: Not working as the schema and/or the base url is bad...
#     result = client.action(schema, action, params=params)
