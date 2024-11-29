import argparse
import torch
from pathlib import Path
from torch.utils.data import DataLoader
from backend.src.services.model_trainer import HandwritingDataset
from backend.src.models.neural_network import SiameseNetwork
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import json

def evaluate_model(model_path: Path, test_data_dir: Path, batch_size: int = 32):
    """Evaluate a trained model on test data.
    
    Args:
        model_path: Path to the saved model
        test_data_dir: Directory containing test images
        batch_size: Batch size for evaluation
    """
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Load model
    model = SiameseNetwork().to(device)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    
    # Create test dataset and loader
    test_dataset = HandwritingDataset(test_data_dir)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    predictions = []
    labels = []
    
    with torch.no_grad():
        for batch in test_loader:
            img1, img2, label = batch
            img1, img2 = img1.to(device), img2.to(device)
            
            # Get predictions
            outputs = model(img1, img2)
            predictions.extend(outputs.cpu().numpy())
            labels.extend(label.cpu().numpy())
    
    # Calculate metrics
    accuracy = accuracy_score(labels, predictions > 0.5)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, predictions > 0.5, average='binary'
    )
    
    metrics = {
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1': float(f1)
    }
    
    return metrics

def main():
    parser = argparse.ArgumentParser(description="Evaluate trained model")
    parser.add_argument("--model_path", type=str, required=True, help="Path to saved model")
    parser.add_argument("--test_data", type=str, required=True, help="Directory containing test data")
    parser.add_argument("--output", type=str, help="Path to save metrics JSON")
    
    args = parser.parse_args()
    
    model_path = Path(args.model_path)
    test_data_dir = Path(args.test_data)
    
    metrics = evaluate_model(model_path, test_data_dir)
    
    # Print metrics
    print("\nEvaluation Metrics:")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.4f}")
    
    # Save metrics if output path provided
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            json.dump(metrics, f, indent=2)
        print(f"\nMetrics saved to: {output_path}")

if __name__ == "__main__":
    main()