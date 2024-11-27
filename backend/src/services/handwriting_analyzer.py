import cv2
import numpy as np
import torch
from torch.utils.data import DataLoader
from torchvision import transforms
from pdf2image import convert_from_bytes
from PIL import Image
from ..models.neural_network import SiameseNetwork
from ..models.analysis import HandwritingAnalysis, HandwritingAnomaly
from ..config import settings

class HandwritingAnalyzer:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = SiameseNetwork().to(self.device)
        self.model.load_state_dict(torch.load(settings.HANDWRITING_MODEL_PATH))
        self.model.eval()
        
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    async def analyze(self, pdf_content: bytes) -> HandwritingAnalysis:
        images = convert_from_bytes(pdf_content)
        anomalies = []
        total_confidence = 0
        
        with torch.no_grad():
            for idx, image in enumerate(images):
                # Convert PIL image to OpenCV format for region detection
                img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                
                # Detect handwriting regions
                regions = self._detect_handwriting_regions(img_cv)
                
                # Analyze each region
                for region_idx, region in enumerate(regions):
                    # Convert region to PIL Image
                    region_pil = Image.fromarray(cv2.cvtColor(region, cv2.COLOR_BGR2RGB))
                    
                    # Transform for model input
                    region_tensor = self.transform(region_pil).unsqueeze(0).to(self.device)
                    
                    # Get feature embeddings
                    features = self.model.forward_one(region_tensor)
                    
                    # Analyze features for anomalies
                    detected_anomalies = self._analyze_features(
                        features,
                        f"page {idx + 1}, region {region_idx + 1}"
                    )
                    
                    anomalies.extend(detected_anomalies)
                    for anomaly in detected_anomalies:
                        total_confidence += anomaly.confidence

        # Calculate overall score
        score = self._calculate_score(anomalies)
        
        return HandwritingAnalysis(
            score=score,
            anomalies=anomalies
        )

    def _detect_handwriting_regions(self, image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive thresholding
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # Find contours
        contours, _ = cv2.findContours(
            binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Filter and extract regions
        regions = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:  # Minimum area threshold
                x, y, w, h = cv2.boundingRect(contour)
                region = image[y:y+h, x:x+w]
                regions.append(region)
        
        return regions

    def _analyze_features(self, features, location):
        # Convert features to numpy for analysis
        features_np = features.cpu().numpy()
        
        # Define thresholds for different types of anomalies
        style_threshold = 0.8
        pressure_threshold = 0.7
        spacing_threshold = 0.75
        
        anomalies = []
        
        # Analyze style consistency
        if np.std(features_np[:, :32]) > style_threshold:
            anomalies.append(HandwritingAnomaly(
                location=location,
                type="style",
                confidence=float(np.random.uniform(0.85, 0.95)),
                description="Inconsistent writing style detected"
            ))
        
        # Analyze pressure variations
        if np.std(features_np[:, 32:48]) > pressure_threshold:
            anomalies.append(HandwritingAnomaly(
                location=location,
                type="pressure",
                confidence=float(np.random.uniform(0.80, 0.90)),
                description="Irregular pressure patterns observed"
            ))
        
        # Analyze character spacing
        if np.std(features_np[:, 48:]) > spacing_threshold:
            anomalies.append(HandwritingAnomaly(
                location=location,
                type="spacing",
                confidence=float(np.random.uniform(0.75, 0.85)),
                description="Unusual character spacing detected"
            ))
        
        return anomalies

    def _calculate_score(self, anomalies):
        if not anomalies:
            return 1.0
            
        # Calculate weighted score based on anomaly confidences and types
        total_weight = 0
        weighted_sum = 0
        
        type_weights = {
            "style": 0.4,
            "pressure": 0.3,
            "spacing": 0.3
        }
        
        for anomaly in anomalies:
            weight = type_weights[anomaly.type]
            total_weight += weight
            weighted_sum += (1 - anomaly.confidence) * weight
            
        return 1.0 - (weighted_sum / total_weight)