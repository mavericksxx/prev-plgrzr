# Data Preparation and Model Training Guide

## Dataset Requirements

### 1. Training Dataset Structure
```
dataset/
├── authentic/
│   ├── doc1_page1.png
│   ├── doc1_page2.png
│   └── ...
├── forged/
│   ├── doc2_page1.png
│   ├── doc2_page2.png
│   └── ...
└── pairs.csv
```

### 2. Data Preparation Steps

1. **Document Preprocessing**
   - Convert PDFs to high-resolution images (300 DPI minimum)
   - Ensure consistent page orientation
   - Apply contrast enhancement if needed
   ```python
   from pdf2image import convert_from_path
   
   # Convert PDFs to images
   images = convert_from_path('document.pdf', dpi=300)
   ```

2. **Image Segmentation**
   - Extract regions of interest:
     - Signatures
     - Handwritten text
     - Printed text
   - Save segments as separate files
   ```python
   import cv2
   
   # Example segmentation
   def segment_document(image):
       gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
       _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
       # Find contours and extract regions
       contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   ```

3. **Labeling**
   Create pairs.csv with the following format:
   ```csv
   image1_path,image2_path,label
   authentic/doc1_p1.png,authentic/doc1_p2.png,1
   authentic/doc1_p1.png,forged/doc2_p1.png,0
   ```

## Model Training Process

### 1. Initialize Training

```python
from backend.src.services.model_trainer import ModelTrainer

trainer = ModelTrainer(
    data_dir='path/to/dataset',
    model_save_path='models/handwriting_model.pt'
)
```

### 2. Training Configuration

```python
training_config = {
    'batch_size': 32,
    'num_epochs': 100,
    'learning_rate': 0.001,
    'weight_decay': 1e-5
}

trainer.train(
    num_epochs=training_config['num_epochs'],
    batch_size=training_config['batch_size']
)
```

### 3. Model Evaluation

```python
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def evaluate_model(model, test_loader):
    model.eval()
    predictions = []
    labels = []
    
    with torch.no_grad():
        for batch in test_loader:
            # Get predictions
            outputs = model(batch['image1'], batch['image2'])
            predictions.extend(outputs.cpu().numpy())
            labels.extend(batch['label'].cpu().numpy())
    
    # Calculate metrics
    accuracy = accuracy_score(labels, predictions > 0.5)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, predictions > 0.5, average='binary'
    )
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }
```

## Training Process

1. **Data Preparation**
   ```bash
   # Create necessary directories
   mkdir -p dataset/{authentic,forged}
   
   # Convert PDFs to images
   python scripts/convert_pdfs.py --input_dir pdfs/ --output_dir dataset/
   
   # Generate training pairs
   python scripts/generate_pairs.py --data_dir dataset/ --output pairs.csv
   ```

2. **Model Training**
   ```bash
   # Train the model
   python -m backend.src.services.model_trainer \
       --data_dir dataset/ \
       --model_save_path models/handwriting_model.pt \
       --epochs 100 \
       --batch_size 32
   ```

3. **Model Evaluation**
   ```bash
   # Evaluate the model
   python scripts/evaluate_model.py \
       --model_path models/handwriting_model.pt \
       --test_data dataset/test/
   ```

## Performance Metrics

Track the following metrics during training:

1. **Document-Level Metrics**
   - Overall authenticity score
   - False positive rate
   - False negative rate

2. **Region-Level Metrics**
   - Segmentation accuracy
   - Region classification accuracy
   - Feature extraction quality

3. **Text Analysis Metrics**
   - OCR accuracy
   - Semantic similarity scores
   - Language model perplexity

## Model Deployment

1. Save the trained model:
   ```python
   torch.save({
       'model_state_dict': model.state_dict(),
       'optimizer_state_dict': optimizer.state_dict(),
       'epoch': epoch,
       'loss': loss,
   }, 'models/handwriting_model.pt')
   ```

2. Load the model in production:
   ```python
   checkpoint = torch.load('models/handwriting_model.pt')
   model.load_state_dict(checkpoint['model_state_dict'])
   model.eval()
   ```

## Next Steps

1. **Data Collection**
   - Gather more authentic documents
   - Create controlled forgeries for training
   - Annotate region boundaries

2. **Model Improvement**
   - Experiment with different architectures
   - Implement data augmentation
   - Add more feature extractors

3. **Evaluation**
   - Create test sets for different document types
   - Measure performance on edge cases
   - Conduct user acceptance testing