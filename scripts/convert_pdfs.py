import argparse
from pathlib import Path
from pdf2image import convert_from_path
import os

def convert_pdf_to_images(pdf_path: Path, output_dir: Path, dpi: int = 300):
    """Convert a PDF file to a series of PNG images.
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save the images
        dpi: Resolution for the output images
    """
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get base name of PDF file (without extension)
    base_name = pdf_path.stem
    
    try:
        # Convert PDF to images
        images = convert_from_path(pdf_path, dpi=dpi)
        
        # Save each page as PNG
        for i, image in enumerate(images):
            image_path = output_dir / f"{base_name}_page{i+1}.png"
            image.save(image_path, "PNG")
            print(f"Saved {image_path}")
            
    except Exception as e:
        print(f"Error converting {pdf_path}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Convert PDFs to images")
    parser.add_argument("--input_dir", type=str, required=True, help="Directory containing PDF files")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save images")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for output images")
    
    args = parser.parse_args()
    
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    
    # Process all PDF files in input directory
    for pdf_file in input_dir.glob("*.pdf"):
        convert_pdf_to_images(pdf_file, output_dir, args.dpi)

if __name__ == "__main__":
    main()