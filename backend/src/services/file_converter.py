import os
from pdf2image import convert_from_bytes
import cv2
import numpy as np
from typing import List, Tuple
from PIL import Image

class FileConverter:
    def __init__(self):
        self.dpi = 300  # High resolution for better analysis
        self.output_format = 'PNG'

    async def pdf_to_images(self, pdf_content: bytes) -> List[np.ndarray]:
        """
        Convert PDF content to a list of OpenCV images.
        
        Args:
            pdf_content (bytes): Raw PDF file content
            
        Returns:
            List[np.ndarray]: List of images in OpenCV format
        """
        try:
            # Convert PDF to PIL Images
            pil_images = convert_from_bytes(
                pdf_content,
                dpi=self.dpi,
                fmt=self.output_format.lower()
            )
            
            # Convert PIL images to OpenCV format
            cv_images = []
            for pil_image in pil_images:
                # Convert PIL image to numpy array
                numpy_image = np.array(pil_image)
                # Convert RGB to BGR for OpenCV
                cv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
                cv_images.append(cv_image)
            
            return cv_images
            
        except Exception as e:
            raise Exception(f"Error converting PDF to images: {str(e)}")

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better analysis.
        
        Args:
            image (np.ndarray): Input image in OpenCV format
            
        Returns:
            np.ndarray: Preprocessed image
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply adaptive histogram equalization
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(gray)
            
            # Denoise
            denoised = cv2.fastNlMeansDenoising(enhanced)
            
            return denoised
            
        except Exception as e:
            raise Exception(f"Error preprocessing image: {str(e)}")

    def extract_regions(self, image: np.ndarray) -> List[Tuple[np.ndarray, str]]:
        """
        Extract different regions from the image.
        
        Args:
            image (np.ndarray): Input image
            
        Returns:
            List[Tuple[np.ndarray, str]]: List of (region_image, region_type) tuples
        """
        try:
            # Convert to binary
            _, binary = cv2.threshold(
                image, 
                0, 
                255, 
                cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )
            
            # Find contours
            contours, _ = cv2.findContours(
                binary,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )
            
            regions = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:  # Minimum area threshold
                    x, y, w, h = cv2.boundingRect(contour)
                    region = image[y:y+h, x:x+w]
                    
                    # Determine region type based on characteristics
                    region_type = self._classify_region(region)
                    
                    regions.append((region, region_type))
            
            return regions
            
        except Exception as e:
            raise Exception(f"Error extracting regions: {str(e)}")

    def _classify_region(self, region: np.ndarray) -> str:
        """
        Classify the type of region based on image characteristics.
        
        Args:
            region (np.ndarray): Region image
            
        Returns:
            str: Region type ('text', 'signature', or 'other')
        """
        # Calculate region characteristics
        height, width = region.shape
        aspect_ratio = width / height
        
        # Calculate pixel density
        pixel_density = np.sum(region > 0) / (width * height)
        
        # Simple classification rules
        if aspect_ratio > 3:  # Long horizontal regions likely text
            return 'text'
        elif 0.5 < aspect_ratio < 2 and pixel_density < 0.2:  # Sparse content might be signature
            return 'signature'
        else:
            return 'other'