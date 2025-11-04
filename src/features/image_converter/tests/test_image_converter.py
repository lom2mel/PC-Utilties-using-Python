from features.image_converter.worker import ImageToPdfWorker
from PIL import Image


def test_image_to_pdf_worker_instantiation(tmp_path):
    """Test that ImageToPdfWorker can be instantiated."""
    image_files = []
    output_path = tmp_path / "output.pdf"
    worker = ImageToPdfWorker(image_files, output_path)
    assert worker is not None


def test_image_to_pdf_worker_run(tmp_path):
    """Test that ImageToPdfWorker creates a PDF file."""
    # Create a dummy image file
    image_file = tmp_path / "test.png"
    img = Image.new("RGB", (100, 100), color="red")
    img.save(image_file)

    image_files = [image_file]
    output_path = tmp_path / "output.pdf"
    worker = ImageToPdfWorker(image_files, output_path)
    worker.run()

    assert output_path.exists()
