"""
Google Translate API engine implementation
"""

from typing import List, Tuple, Optional
from googletrans import Translator, LANGUAGES
from lingosnap.engines.base import TranslationEngine


class GoogleTranslateEngine(TranslationEngine):
    """Google Translate API engine for online translation"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Google Translate engine
        
        Args:
            api_key: Google Translate API key (optional for now)
        """
        self.api_key = api_key
        self.translator = Translator()
        self.character_count = 0
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text using Google Translate
        
        Args:
            text: Text to translate
            source_lang: Source language code (e.g., 'en')
            target_lang: Target language code (e.g., 'zh-cn')
            
        Returns:
            Translated text
        """
        try:
            # Handle auto-detection
            if source_lang == 'auto':
                result = self.translator.translate(text, dest=target_lang)
            else:
                result = self.translator.translate(text, src=source_lang, dest=target_lang)
            
            # Update character count
            self.character_count += len(text)
            
            return result.text
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")
    
    def get_supported_languages(self) -> List[Tuple[str, str]]:
        """
        Get list of supported languages
        
        Returns:
            List of tuples (language_code, language_name)
        """
        # Return all Google Translate supported languages
        return sorted([(code, name.capitalize()) for code, name in LANGUAGES.items()], 
                     key=lambda x: x[1])
    
    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect the language of the given text
        
        Args:
            text: Text to analyze
            
        Returns:
            Language code or None if detection fails
        """
        try:
            detection = self.translator.detect(text)
            return detection.lang
        except Exception:
            return None
    
    def is_available(self) -> bool:
        """
        Check if Google Translate is available
        
        Returns:
            True if available (always True for googletrans library)
        """
        return True
    
    def get_character_count(self) -> int:
        """
        Get the total number of characters translated
        
        Returns:
            Character count
        """
        return self.character_count
    
    def reset_character_count(self):
        """Reset the character count to zero"""
        self.character_count = 0
