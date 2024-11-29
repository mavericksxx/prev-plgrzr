import argparse
from pathlib import Path
import csv
import itertools

def generate_pairs(data_dir: Path, output_file: Path):
    """Generate pairs of images for training.
    
    Args:
        data_dir: Directory containing authentic and forged subdirectories
        output_file: Path to save the pairs CSV file
    """
    authentic_dir = data_dir / "authentic"
    forged_dir = data_dir / "forged"
    
    # Get lists of images
    authentic_images = list(authentic_dir.glob("*.png"))
    forged_images = list(forged_dir.glob("*.png"))
    
    # Open output file
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["image1", "image2", "label"])
        
        # Generate positive pairs (same document)
        for img1, img2 in itertools.combinations(authentic_images, 2):
            if img1.stem.split("_page")[0] == img2.stem.split("_page")[0]:
                writer.writerow([str(img1), str(img2), 1])
        
        # Generate negative pairs (different documents)
        for auth_img in authentic_images:
            for forged_img in forged_images:
                writer.writerow([str(auth_img), str(forged_img), 0])

def main():
    parser = argparse.ArgumentParser(description="Generate image pairs for training")
    parser.add_argument("--data_dir", type=str, required=True, help="Directory containing authentic and forged subdirectories")
    parser.add_argument("--output", type=str, required=True, help="Output CSV file")
    
    args = parser.parse_args()
    
    data_dir = Path(args.data_dir)
    output_file = Path(args.output)
    
    generate_pairs(data_dir, output_file)
    print(f"Pairs file generated: {output_file}")

if __name__ == "__main__":
    main()