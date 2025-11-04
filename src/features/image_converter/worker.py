from PySide6.QtCore import QThread, Signal
from PIL import Image
from pathlib import Path


class ImageToPdfWorker(QThread):
    """Worker thread for converting images to PDF"""

    progress = Signal(int, int, str)  # current, total, current_file
    finished = Signal(dict)  # results dictionary

    def __init__(self, image_files, output_path):
        super().__init__()
        self.image_files = image_files
        self.output_path = output_path
        self.cancelled = False

    def run(self):
        """Execute the image to PDF conversion"""
        results = {"success": False, "error": None, "output_path": self.output_path}

        try:
            # Convert images to PDF
            images = []

            for idx, image_file in enumerate(self.image_files):
                if self.cancelled:
                    results["error"] = "Conversion cancelled by user"
                    break

                self.progress.emit(idx + 1, len(self.image_files), str(image_file))

                try:
                    # Open and convert image
                    img = Image.open(image_file)

                    # Convert to RGB if necessary (PDF doesn't support RGBA or other modes)
                    if img.mode in ("RGBA", "LA", "P"):
                        # Create white background
                        background = Image.new("RGB", img.size, (255, 255, 255))
                        if img.mode == "P":
                            img = img.convert("RGBA")
                        background.paste(
                            img,
                            mask=img.split()[-1]
                            if img.mode in ("RGBA", "LA")
                            else None,
                        )
                        img = background
                    elif img.mode != "RGB":
                        img = img.convert("RGB")

                    images.append(img)
                except Exception as e:
                    results["error"] = (
                        f"Error processing {Path(image_file).name}: {str(e)}"
                    )
                    break

            if images and not self.cancelled:
                # Save as PDF
                if len(images) == 1:
                    images[0].save(self.output_path, "PDF", resolution=100.0)
                else:
                    images[0].save(
                        self.output_path,
                        "PDF",
                        resolution=100.0,
                        save_all=True,
                        append_images=images[1:],
                    )

                results["success"] = True

        except Exception as e:
            results["error"] = str(e)

        self.finished.emit(results)

    def cancel(self):
        """Cancel the conversion process"""
        self.cancelled = True
