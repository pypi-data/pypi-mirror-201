import datetime
import os
from shutil import copytree, rmtree
from unittest import TestCase

from asterism import file_helpers


class TestFileHelpers(TestCase):
    def setUp(self):
        self.fixtures_dir = os.path.join(
            os.getcwd(), 'asterism', 'fixtures')
        self.file_path = os.path.join(
            self.fixtures_dir, 'file_helpers', 'file.txt')
        self.dir_path = os.path.join(
            self.fixtures_dir, 'file_helpers', 'directory')
        self.tmp_dir = os.path.join(self.fixtures_dir, 'tmp')

    def test_file_attributes(self):
        for fp in os.listdir(self.fixtures_dir):
            path = os.path.join(self.fixtures_dir, fp)
            owner = file_helpers.get_owner(path)
            self.assertIsNot(False, owner)
            mtime = file_helpers.get_modified_time(path)
            self.assertTrue(isinstance(mtime, datetime.datetime))
            exists = file_helpers.is_dir_or_file(path)
            self.assertTrue(exists)

        size = file_helpers.get_dir_size(self.dir_path)
        self.assertIsNot(False, size)
        self.assertTrue(size > 0)

    def test_file_actions(self):
        target_path = os.path.join(self.tmp_dir, "directory")
        copied = file_helpers.copy_file_or_dir(self.dir_path, target_path)
        self.assertTrue(copied)
        self.assertTrue(os.path.isdir(target_path))
        self.assertTrue(os.path.isdir(self.dir_path))

        target_path = os.path.join(
            self.tmp_dir, os.path.join(self.tmp_dir, os.path.basename(self.file_path)))
        copied = file_helpers.copy_file_or_dir(self.file_path, target_path)
        self.assertTrue(copied)
        self.assertTrue(os.path.isfile(target_path))
        self.assertTrue(os.path.isfile(self.file_path))

        for path in [os.path.basename(
                self.file_path), os.path.basename(self.dir_path)]:
            moved = file_helpers.move_file_or_dir(
                os.path.join(self.tmp_dir, path), os.path.join(self.tmp_dir, "moved", path))
            self.assertTrue(moved)

        for path in os.listdir(os.path.join(self.tmp_dir, "moved")):
            removed = file_helpers.remove_file_or_dir(
                os.path.join(self.tmp_dir, "moved", path))
            self.assertTrue(removed)

    def test_make_tarfile(self):
        src_path = os.path.join(self.fixtures_dir, "file_helpers", "archive")
        for remove_src in [False, True]:
            for fp, compressed in [
                    ("archive.tar", False), ("archive.tar.gz", True)]:
                if not os.path.isdir(src_path):
                    copytree(self.dir_path, src_path)
                tarfile = file_helpers.make_tarfile(
                    src_path,
                    os.path.join(self.tmp_dir, fp),
                    compressed=compressed,
                    remove_src=remove_src)
                self.assertTrue(tarfile)

    def test_extract_serialized(self):
        for f in [
                "directory", "directory.zip",
                "directory.tar", "directory.tar.gz"]:
            extracted = file_helpers.anon_extract_all(
                os.path.join(self.fixtures_dir, "file_helpers", f), self.tmp_dir)
            self.assertTrue(extracted)
            self.assertTrue(os.path.isdir(extracted))

    def tearDown(self):
        if os.path.isdir(self.tmp_dir):
            rmtree(self.tmp_dir)
