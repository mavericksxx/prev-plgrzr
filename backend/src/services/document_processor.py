from ..models.analysis import AnalysisResult
from .visual_analyzer import VisualAnalyzer
from .text_analyzer import TextAnalyzer
from .handwriting_analyzer import HandwritingAnalyzer
from .file_converter import FileConverter
import asyncio

class DocumentProcessor:
    def __init__(self):
        self.file_converter = FileConverter()
        self.visual_analyzer = VisualAnalyzer()
        self.text_analyzer = TextAnalyzer()
        self.handwriting_analyzer = HandwritingAnalyzer()

    async def analyze(self, pdf_content: bytes) -> AnalysisResult:
        # Convert PDF to images
        images = await self.file_converter.pdf_to_images(pdf_content)
        
        # Process each image
        processed_images = []
        for image in images:
            # Preprocess the image
            preprocessed = self.file_converter.preprocess_image(image)
            # Extract regions
            regions = self.file_converter.extract_regions(preprocessed)
            processed_images.append((preprocessed, regions))

        # Run analyses concurrently
        visual_task = asyncio.create_task(
            self.visual_analyzer.analyze(processed_images)
        )
        text_task = asyncio.create_task(
            self.text_analyzer.analyze(processed_images)
        )
        handwriting_task = asyncio.create_task(
            self.handwriting_analyzer.analyze(processed_images)
        )

        # Wait for all analyses to complete
        visual_result = await visual_task
        text_result = await text_task
        handwriting_result = await handwriting_task

        # Calculate overall score
        overall_score = (
            visual_result.score * 0.4 +
            text_result.score * 0.3 +
            handwriting_result.score * 0.3
        )

        return AnalysisResult(
            visual_similarity=visual_result,
            text_analysis=text_result,
            handwriting_analysis=handwriting_result,
            overall_score=overall_score
        )