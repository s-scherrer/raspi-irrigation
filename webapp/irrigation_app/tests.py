from django.test import TestCase
import pytest

from .models import Observable


@pytest.mark.django_db
class IrrigationAppTest(TestCase):

    def test_observables():
        observables = Observable.objects.order_by('id').all()

        assert observables[0].short_name == "rh"
        assert observables[1].short_name == "ta"
