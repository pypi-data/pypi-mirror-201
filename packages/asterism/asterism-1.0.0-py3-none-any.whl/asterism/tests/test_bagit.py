import os
from random import sample
from shutil import copytree, rmtree
from unittest import TestCase

import bagit
from asterism import bagit_helpers


class TestBagitHelpers(TestCase):
    def setUp(self):
        self.bag_path = os.path.join(
            os.getcwd(), 'asterism', 'fixtures', 'test_bag')
        if os.path.isdir(self.bag_path):
            rmtree(self.bag_path)
        copytree(
            os.path.join(os.getcwd(), 'asterism', 'fixtures', 'bag'),
            self.bag_path)
        bagit.make_bag(self.bag_path)

    def remove_random_file(self, dir):
        for f in sample(os.listdir(dir), 1):
            os.remove(os.path.join(dir, f))

    def test_validate(self):
        valid = bagit_helpers.validate(self.bag_path)
        self.assertEqual(valid, True)
        self.remove_random_file(os.path.join(self.bag_path, 'data'))
        with self.assertRaises(bagit.BagValidationError):
            bagit_helpers.validate(self.bag_path)

    def test_update_bag_info(self):
        key = "foo"
        value = "bar"
        bagit_helpers.update_bag_info(self.bag_path, {key: value})
        bag = bagit.Bag(self.bag_path)
        self.assertEqual(bag.info[key], value)
        with self.assertRaises(AssertionError):
            bagit_helpers.update_bag_info(self.bag_path, [key, value])

    def test_update_manifests(self):
        self.remove_random_file(os.path.join(self.bag_path, 'data'))
        bagit_helpers.update_manifests(self.bag_path)
        bag = bagit.Bag(self.bag_path)
        self.assertTrue(bag.validate())

    def test_get_bag_info_fields(self):
        fields = bagit_helpers.get_bag_info_fields(self.bag_path)
        self.assertTrue(
            isinstance(
                fields,
                dict),
            "Incorrect bag-info data: {}".format(fields))
        for key in ["Bag_Software_Agent", "Bagging_Date", "Payload_Oxum"]:
            self.assertTrue(key in fields.keys())

    def tearDown(self):
        rmtree(self.bag_path)
