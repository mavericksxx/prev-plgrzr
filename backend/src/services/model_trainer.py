import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
import numpy as np
from pathlib import Path
from ..models.neural_network import SiameseNetwork

class HandwritingDataset(Dataset):
    def __init__(self, data_dir: str, transform=None):
        self.data_dir = Path(data_dir)
        self.transform = transform or transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        # Load and preprocess images
        self.images = list(self.data_dir.glob('*.png'))
        
    def __len__(self):
        return len(self.images)
        
    def __getitem__(self, idx):
        img_path = self.images[idx]
        image = Image.open(img_path).convert('RGB')
        
        if self.transform:
            image = self.transform(image)
            
        # For training, create positive and negative pairs
        # This is a simplified version - in production, use actual pairs
        return image

class ModelTrainer:
    def __init__(self, data_dir: str, model_save_path: str):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = SiameseNetwork().to(self.device)
        self.criterion = nn.ContrastiveLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.data_dir = data_dir
        self.model_save_path = model_save_path
        
    def train(self, num_epochs: int = 10, batch_size: int = 32):
        dataset = HandwritingDataset(self.data_dir)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        for epoch in range(num_epochs):
            running_loss = 0.0
            for i, data in enumerate(dataloader):
                # Get pairs of images
                img1, img2 = data  # In practice, implement proper pair selection
                img1, img2 = img1.to(self.device), img2.to(self.device)
                
                # Forward pass
                self.optimizer.zero_grad()
                output = self.model(img1, img2)
                
                # Compute loss (simplified - implement proper loss calculation)
                loss = self.criterion(output, torch.ones_like(output))
                
                # Backward pass and optimize
                loss.backward()
                self.optimizer.step()
                
                running_loss += loss.item()
                
            print(f'Epoch {epoch + 1}, Loss: {running_loss / len(dataloader)}')
            
        # Save the trained model
        torch.save(self.model.state_dict(), self.model_save_path)
        print(f'Model saved to {self.model_save_path}')