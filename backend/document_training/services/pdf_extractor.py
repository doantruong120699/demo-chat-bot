"""
PDF Text Extraction Service
"""
import logging
from typing import Optional
import io

logger = logging.getLogger(__name__)


class PDFExtractor:
    """Service to extract text from PDF files"""
    
    @staticmethod
    def extract_text(pdf_file) -> Optional[str]:
        """
        Extract text from PDF file
        
        Args:
            pdf_file: Django UploadedFile object
            
        Returns:
            Extracted text string or None if failed
        """
        try:
            # Try pdfplumber first (better for complex PDFs)
            try:
                import pdfplumber
                
                logger.info(f"📄 Extracting PDF with pdfplumber: {pdf_file.name}")
                
                # Read file content
                pdf_bytes = pdf_file.read()
                pdf_file.seek(0)  # Reset file pointer
                
                text_parts = []
                with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                    for page_num, page in enumerate(pdf.pages, 1):
                        page_text = page.extract_text()
                        if page_text:
                            text_parts.append(page_text)
                            logger.info(f"  ✅ Page {page_num}: {len(page_text)} chars")
                        else:
                            logger.warning(f"  ⚠️ Page {page_num}: No text extracted")
                
                full_text = "\n\n".join(text_parts)
                logger.info(f"✅ Total extracted: {len(full_text)} chars from {len(text_parts)} pages")
                return full_text
                
            except ImportError:
                logger.warning("pdfplumber not available, falling back to PyPDF2")
                
                # Fallback to PyPDF2
                import PyPDF2
                
                logger.info(f"📄 Extracting PDF with PyPDF2: {pdf_file.name}")
                
                # Read file content
                pdf_bytes = pdf_file.read()
                pdf_file.seek(0)  # Reset file pointer
                
                text_parts = []
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
                        logger.info(f"  ✅ Page {page_num}: {len(page_text)} chars")
                    else:
                        logger.warning(f"  ⚠️ Page {page_num}: No text extracted")
                
                full_text = "\n\n".join(text_parts)
                logger.info(f"✅ Total extracted: {len(full_text)} chars from {len(text_parts)} pages")
                return full_text
                
        except Exception as e:
            logger.error(f"❌ PDF extraction failed: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    @staticmethod
    def is_pdf(file) -> bool:
        """Check if file is PDF"""
        return (
            file.content_type == 'application/pdf' or 
            file.name.lower().endswith('.pdf')
        )
