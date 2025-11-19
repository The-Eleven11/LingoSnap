"""
Argos Translate engine implementation
"""

from typing import List, Tuple, Optional
import argostranslate.package
import argostranslate.translate
from lingosnap.engines.base import TranslationEngine


class ArgosTranslateEngine(TranslationEngine):
    """Argos Translate engine for offline translation"""
    
    def __init__(self):
        """Initialize Argos Translate engine"""
        # Update package index
        try:
            argostranslate.package.update_package_index()
        except Exception:
            pass  # Ignore errors during initialization
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text using Argos Translate
        
        Args:
            text: Text to translate
            source_lang: Source language code (e.g., 'en')
            target_lang: Target language code (e.g., 'zh')
            
        Returns:
            Translated text
        """
        try:
            # Argos uses 2-letter codes
            translated = argostranslate.translate.translate(text, source_lang, target_lang)
            return translated if translated else text
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")
    
    def get_supported_languages(self) -> List[Tuple[str, str]]:
        """
        Get list of installed language packages
        
        Returns:
            List of tuples (language_code, language_name)
        """
        installed_languages = argostranslate.package.get_installed_packages()
        
        # Get unique languages from installed packages
        languages = set()
        for pkg in installed_languages:
            languages.add((pkg.from_code, pkg.from_name))
            languages.add((pkg.to_code, pkg.to_name))
        
        return sorted(list(languages), key=lambda x: x[1])
    
    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect language (basic implementation)
        Note: Argos doesn't have built-in language detection
        
        Args:
            text: Text to analyze
            
        Returns:
            Language code or None
        """
        # Simple heuristic: check if text contains Chinese characters
        if any('\u4e00' <= char <= '\u9fff' for char in text):
            return 'zh'
        # Default to English
        return 'en'
    
    def is_available(self) -> bool:
        """
        Check if Argos Translate is available with installed packages
        
        Returns:
            True if packages are installed
        """
        try:
            packages = argostranslate.package.get_installed_packages()
            return len(packages) > 0
        except Exception:
            return False
    
    def get_installed_packages(self) -> List[dict]:
        """
        Get list of installed language packages
        
        Returns:
            List of package information dictionaries
        """
        packages = argostranslate.package.get_installed_packages()
        return [
            {
                'from_code': pkg.from_code,
                'from_name': pkg.from_name,
                'to_code': pkg.to_code,
                'to_name': pkg.to_name,
                'package_version': pkg.package_version
            }
            for pkg in packages
        ]
    
    def get_available_packages(self) -> List[dict]:
        """
        Get list of available packages for download
        
        Returns:
            List of available package information
        """
        try:
            argostranslate.package.update_package_index()
            available_packages = argostranslate.package.get_available_packages()
            return [
                {
                    'from_code': pkg.from_code,
                    'from_name': pkg.from_name,
                    'to_code': pkg.to_code,
                    'to_name': pkg.to_name,
                    'package_version': pkg.package_version
                }
                for pkg in available_packages
            ]
        except Exception:
            return []
    
    def install_package(self, from_code: str, to_code: str) -> bool:
        """
        Install a language package
        
        Args:
            from_code: Source language code
            to_code: Target language code
            
        Returns:
            True if installation succeeded
        """
        try:
            argostranslate.package.update_package_index()
            available_packages = argostranslate.package.get_available_packages()
            
            # Find the package
            package_to_install = None
            for pkg in available_packages:
                if pkg.from_code == from_code and pkg.to_code == to_code:
                    package_to_install = pkg
                    break
            
            if package_to_install:
                argostranslate.package.install_from_path(package_to_install.download())
                return True
            return False
        except Exception:
            return False
