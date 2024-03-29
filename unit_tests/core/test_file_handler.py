from unittest import mock
from os import path

import pytest
from core.file_handler import SafeS3FileUploadHandler
from s3chunkuploader.file_handler import UploadFailed


TEST_FILES_PATH = path.join(path.dirname(__file__), "test_file_handler_files")


@pytest.fixture
def mock_handler():
    handler = SafeS3FileUploadHandler()
    handler.file = mock.Mock()
    handler.client = mock.Mock()
    handler.executor = mock.Mock()
    handler.bucket_name = "test"
    handler.s3_key = "test"
    handler.upload_id = "test"
    return handler


def test_valid_file_upload(mock_handler):
    with open(f"{TEST_FILES_PATH}/valid.txt", "rb") as f:
        content = f.read()
        mock_handler.abort = mock.Mock()
        mock_handler.receive_data_chunk(content, 0)
        mock_handler.abort.assert_not_called
        # set start to be anything but 0
        mock_handler.receive_data_chunk(content, 1)
        mock_handler.abort.assert_not_called


def test_invalid_file_type_upload(mock_handler):
    with open(f"{TEST_FILES_PATH}/invalid_type.zip", "rb") as f:
        content = f.read()
        with pytest.raises(UploadFailed):
            mock_handler.receive_data_chunk(content, 0)


def test_invalid_file_mime_type_upload(mock_handler):
    with open(f"{TEST_FILES_PATH}/invalid_mime.txt", "rb") as f:
        content = f.read()
        with pytest.raises(UploadFailed):
            mock_handler.receive_data_chunk(content, 0)
