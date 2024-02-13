import pytest


def test_django_loads():
    from django.conf import settings

    assert len(settings.INSTALLED_APPS) > 0


@pytest.mark.django_db
def test_db_connection(django_user_model):
    assert django_user_model.objects.all().count() == 0
