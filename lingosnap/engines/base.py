"""
Abstract base class for translation engines
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional


class TranslationEngine(ABC):
    """Abstract base class for translation engines"""
    
    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text from source language to target language
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        pass
    
    @abstractmethod
    def get_supported_languages(self) -> List[Tuple[str, str]]:
        """
        Get list of supported languages
        
        Returns:
            List of tuples (language_code, language_name)
        """
        pass
    
    @abstractmethod
    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect the language of the given text
        
        Args:
            text: Text to analyze
            
        Returns:
            Language code or None if detection fails
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the engine is available and properly configured
        
        Returns:
            True if engine is available, False otherwise
        """
        pass
