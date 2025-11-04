from unittest.mock import patch
from features.office_converter.worker import ConversionWorker


def test_conversion_worker_instantiation(tmp_path):
    """Test that ConversionWorker can be instantiated."""
    path = tmp_path
    worker = ConversionWorker(path)
    assert worker is not None


@patch("features.office_converter.worker.ConversionWorker.convert_file")
def test_conversion_worker_run(mock_convert_file, tmp_path):
    """Test that ConversionWorker's run method calls convert_file."""
    # Create a dummy file
    file_path = tmp_path / "test.doc"
    file_path.touch()

    worker = ConversionWorker(str(tmp_path), is_file=False)
    worker.run()

    mock_convert_file.assert_called_once_with(file_path)
