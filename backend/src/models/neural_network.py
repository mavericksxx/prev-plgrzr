import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models

class HandwritingCNN(nn.Module):
    def __init__(self):
        super(HandwritingCNN, self).__init__()
        # Use ResNet18 as the base model, pre-trained on ImageNet
        resnet = models.resnet18(pretrained=True)
        # Remove the last fully connected layer
        self.features = nn.Sequential(*list(resnet.children())[:-1])
        
        # Add custom layers for handwriting analysis
        self.fc1 = nn.Linear(512, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 64)
        
        # Output layers for different aspects
        self.style_head = nn.Linear(64, 32)
        self.pressure_head = nn.Linear(64, 16)
        self.spacing_head = nn.Linear(64, 16)
        
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        # Extract features using ResNet
        x = self.features(x)
        x = x.view(x.size(0), -1)
        
        # Common feature processing
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        x = F.relu(self.fc3(x))
        
        # Specialized outputs
        style = torch.sigmoid(self.style_head(x))
        pressure = torch.sigmoid(self.pressure_head(x))
        spacing = torch.sigmoid(self.spacing_head(x))
        
        return style, pressure, spacing

class SiameseNetwork(nn.Module):
    def __init__(self):
        super(SiameseNetwork, self).__init__()
        self.cnn = HandwritingCNN()
        self.distance_layer = nn.CosineSimilarity(dim=1)
        
    def forward_one(self, x):
        style, pressure, spacing = self.cnn(x)
        features = torch.cat([style, pressure, spacing], dim=1)
        return features
        
    def forward(self, x1, x2):
        # Get features for both images
        output1 = self.forward_one(x1)
        output2 = self.forward_one(x2)
        
        # Calculate similarity score
        similarity = self.distance_layer(output1, output2)
        return similarity