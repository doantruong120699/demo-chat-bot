"""
OCR Service for extracting text from images and PDFs
Supports: camera scan, image upload, PDF files
"""
from PIL import Image
import pytesseract
import PyPDF2
import io
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class OCRService:
    """Service to extract text from various sources"""
    
    @staticmethod
    def extract_from_image(image_file) -> Dict[str, Any]:
        """
        Extract text from image using Tesseract OCR
        
        Args:
            image_file: Django UploadedFile or file path
            
        Returns:
            dict with 'text', 'language', 'confidence'
        """
        try:
            # Open image
            image = Image.open(image_file)
            
            # Perform OCR
            # Config for Vietnamese + English
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(image, lang='vie+eng', config=custom_config)
            
            # Get confidence
            data = pytesseract.image_to_data(image, lang='vie+eng', output_type=pytesseract.Output.DICT)
            confidences = [int(conf) for conf in data['conf'] if conf != '-1']
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                'text': text.strip(),
                'language': 'vi',
                'confidence': avg_confidence,
                'success': True,
                'page_count': 1,
            }
            
        except Exception as e:
            logger.error(f"OCR extraction failed: {str(e)}")
            return {
                'text': '',
                'success': False,
                'error': str(e),
            }
    
    @staticmethod
    def extract_from_pdf(pdf_file) -> Dict[str, Any]:
        """
        Extract text from PDF file
        
        Args:
            pdf_file: Django UploadedFile or file path
            
        Returns:
            dict with 'text', 'page_count', 'success'
        """
        try:
            # Read PDF
            if hasattr(pdf_file, 'read'):
                pdf_data = pdf_file.read()
                pdf_file.seek(0)  # Reset file pointer
            else:
                with open(pdf_file, 'rb') as f:
                    pdf_data = f.read()
            
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_data))
            page_count = len(pdf_reader.pages)
            
            # Extract text from all pages
            text_parts = []
            for page_num, page in enumerate(pdf_reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(f"[Page {page_num}]\n{page_text}")
            
            full_text = "\n\n".join(text_parts)
            
            return {
                'text': full_text.strip(),
                'page_count': page_count,
                'success': True,
                'language': 'vi',  # Assume Vietnamese for now
            }
            
        except Exception as e:
            logger.error(f"PDF extraction failed: {str(e)}")
            return {
                'text': '',
                'success': False,
                'error': str(e),
            }
    
    @staticmethod
    def extract_text(file, source_type: str) -> Dict[str, Any]:
        """
        Main entry point for text extraction
        
        Args:
            file: Django UploadedFile
            source_type: 'IMAGE', 'PDF', 'CAMERA', 'TEXT'
            
        Returns:
            dict with extraction results
        """
        if source_type == 'TEXT':
            # Plain text, just read it
            text = file.read().decode('utf-8')
            return {
                'text': text,
                'success': True,
                'page_count': 1,
                'language': 'vi',
            }
        
        elif source_type in ['IMAGE', 'CAMERA']:
            return OCRService.extract_from_image(file)
        
        elif source_type == 'PDF':
            return OCRService.extract_from_pdf(file)
        
        else:
            return {
                'text': '',
                'success': False,
                'error': f'Unsupported source type: {source_type}',
            }
