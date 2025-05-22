"""Contains tests for the MinIO storage backend."""

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import TestCase


class MinioStorageTest(TestCase):
    """Test case for MinIO storage backend."""

    def test_file_save_and_read(self) -> None:
        """Test saving and reading a file from MinIO storage."""
        filename = "testfile2.txt"
        content = b"Hello, MinIO from Django test!"

        # Save a file
        file_obj = ContentFile(content)
        saved_name = default_storage.save(filename, file_obj)

        # Make sure the filename is returned
        self.assertEqual(saved_name, filename)

        # Check that the file exists in storage
        self.assertTrue(default_storage.exists(filename))

        # Read file back from storage
        with default_storage.open(filename) as f:
            read_content = f.read()

        # Verify the content is the same
        self.assertEqual(read_content, content)

        # Clean up: delete the file from storage
