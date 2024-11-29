# Document Verification Workflow

## 1. Organize Your Data

The dataset structure should look like this:

dataset/  
├── authentic/      # Put 70 authentic PDFs here (70% for training)  
├── forged/         # Put 30 forged PDFs here (30% for training)  
└── test/           # Keep 10-15 PDFs for testing (not used in training)

## 2. Convert PDFs to Images

Convert authentic documents:  
`python scripts/convert_pdfs.py --input_dir dataset/authentic --output_dir dataset/authentic`  

Convert forged documents:  
`python scripts/convert_pdfs.py --input_dir dataset/forged --output_dir dataset/forged`  

Convert test documents:  
`python scripts/convert_pdfs.py --input_dir dataset/test --output_dir dataset/test`  

## 3. Generate Training Pairs

Run the following command to create pairs of images for comparison:  
`python scripts/generate_pairs.py --data_dir dataset --output dataset/pairs.csv`  

- **Positive pairs:** Pages from the same authentic document  
- **Negative pairs:** Pages from authentic vs forged documents  

## 4. Train the Model

Use this command to train the model:  
`python -m backend.src.services.model_trainer --data_dir dataset --model_save_path models/handwriting_model.pt --epochs 100 --batch_size 32`  

### Training Details:
- **Batch size:** Use `batch_size=32` (a good balance for memory).  
- **Epochs:** Train for **100 epochs** initially.  

### Training Notes:
- Training might take **2-3 hours**, depending on your machine.  

## 5. Evaluate the Model

Run the evaluation script:  
`python scripts/evaluate_model.py --model_path models/handwriting_model.pt --test_data dataset/test --output metrics.json`  

## Important Tips

- Ensure your PDFs are **high quality** and scanned at **300 DPI minimum**.  
- Keep consistent **page orientation** for each PDF.  
- Use meaningful file names (e.g., `authentic_doc1.pdf`, `forged_doc1.pdf`).  

### For Better Accuracy:
- Monitor training progress. Stop early if accuracy plateaus.  
- If accuracy is low, try:  
  - Increasing training epochs  
  - Adjusting batch size  
  - Adding more training data  
  - Cleaning up low-quality scans  