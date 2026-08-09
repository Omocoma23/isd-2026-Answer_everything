from pathlib import Path
from pdf2image import convert_from_path, pdfinfo_from_path
import cv2
from PIL import Image
from .utils.io import ensure_dir

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


def is_image(path: str | Path) -> bool:
    return Path(path).suffix.lower() in IMAGE_EXTENSIONS


def is_pdf(path: str | Path) -> bool:
    return Path(path).suffix.lower() == ".pdf"


def pdf_to_images(pdf_path, output_dir, dpi=200, batch_size=8):
    """Convert a large PDF in small batches so a 400+ page PDF does not fill RAM."""
    pdf_path = Path(pdf_path)
    output_dir = ensure_dir(output_dir)

    info = pdfinfo_from_path(str(pdf_path))
    total_pages = int(info["Pages"])

    image_paths = []

    for first_page in range(1, total_pages + 1, batch_size):
        last_page = min(first_page + batch_size - 1, total_pages)

        pages = convert_from_path(
            str(pdf_path),
            dpi=dpi,
            first_page=first_page,
            last_page=last_page,
            fmt="jpeg",
            thread_count=1,
        )

        for offset, page_image in enumerate(pages):
            page_no = first_page + offset
            out = output_dir / f"{pdf_path.stem}_page_{page_no:03d}.jpg"
            page_image.save(out, "JPEG", quality=92)
            image_paths.append(out)

        # pages is released every batch instead of keeping all 403 pages in RAM
        del pages

    return image_paths

def load_document_pages(input_path: str | Path, output_dir: str | Path, dpi: int = 300) -> list[Path]:
    input_path = Path(input_path)
    if is_pdf(input_path):
        return pdf_to_images(input_path, output_dir, dpi=dpi)
    if is_image(input_path):
        return [input_path]
    raise ValueError(f"Unsupported file type: {input_path.suffix}")
