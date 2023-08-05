import random
from unittest import TestCase

from django.core.exceptions import ValidationError

from .helpers import configure_django, random_string

# this has to be called before we try to import models
configure_django()

from asterism.models import BasePackage


class Package(BasePackage):
    STARTED = 10
    COMPLETED = 20
    PROCESS_STATUS_CHOICES = (
        (STARTED, "Started"),
        (COMPLETED, "Completed")
    )


class TestModels(TestCase):

    def test_base_package(self):
        # Required fields only
        package = Package(
            bag_identifier=random_string(255),
            bag_path=random_string(255),
            origin=random.choice(BasePackage.ORIGIN_CHOICES)[0],
            process_status=random.choice(Package.PROCESS_STATUS_CHOICES)[0],
        )
        self.assertTrue(isinstance(package, Package))
        package.clean_fields()

        # Additional fields
        package.type = random.choice(BasePackage.TYPE_CHOICES)[0]
        package.data = {random_string(): random_string(20)}
        self.assertTrue(isinstance(package, Package))
        package.clean_fields()

        # Make sure choices are enforced
        for field in ["origin", "process_status", "type"]:
            invalid_package = package
            setattr(invalid_package, field, "wrong")
            self.assertTrue(isinstance(invalid_package, Package))
            with self.assertRaises(ValidationError):
                invalid_package.clean_fields()
