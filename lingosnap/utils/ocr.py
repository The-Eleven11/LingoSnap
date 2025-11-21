"""
OCR functionality using Tesseract
"""

import pytesseract
from PIL import Image
from typing import Optional


class OCREngine:
    """OCR engine using Tesseract"""
    
    def __init__(self):
        """Initialize OCR engine"""
        self.tesseract_cmd = None
    
    def set_tesseract_path(self, path: str):
        """
        Set custom Tesseract executable path
        
        Args:
            path: Path to tesseract executable
        """
        self.tesseract_cmd = path
        pytesseract.pytesseract.tesseract_cmd = path
    
    def extract_text(self, image: Image.Image, lang: str = 'eng') -> str:
        """
        Extract text from image using OCR
        
        Args:
            image: PIL Image object
            lang: Language code for OCR (default: 'eng')
            
        Returns:
            Extracted text
        """
        try:
            # Perform OCR with optimized config for faster processing
            # PSM 3 = Fully automatic page segmentation (default)
            # OEM 3 = Default OCR Engine Mode (best available)
            config = '--psm 3 --oem 3'
            
            # Add timeout to prevent hanging
            # Tesseract can sometimes hang on certain images
            text = pytesseract.image_to_string(
                image, 
                lang=lang,
                config=config,
                timeout=30  # 30 second timeout
            )
            return text.strip()
        except pytesseract.TesseractError as e:
            # Tesseract-specific error
            raise Exception(f"OCR failed: {str(e)}")
        except Exception as e:
            # Other errors (including timeout)
            raise Exception(f"OCR failed: {str(e)}")
    
    def extract_text_from_file(self, image_path: str, lang: str = 'eng') -> str:
        """
        Extract text from image file
        
        Args:
            image_path: Path to image file
            lang: Language code for OCR (default: 'eng')
            
        Returns:
            Extracted text
        """
        try:
            image = Image.open(image_path)
            return self.extract_text(image, lang)
        except Exception as e:
            raise Exception(f"Failed to read image: {str(e)}")
    
    def is_available(self) -> bool:
        """
        Check if Tesseract is available
        
        Returns:
            True if Tesseract is installed and accessible
        """
        try:
            pytesseract.get_tesseract_version()
            return True
        except Exception:
            return False
    
    def get_available_languages(self) -> list:
        """
        Get list of available OCR languages
        
        Returns:
            List of language codes
        """
        try:
            langs = pytesseract.get_languages()
            return langs
        except Exception:
            return ['eng']  # Default to English
