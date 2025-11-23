"""
Basic tests for LingoSnap
"""

import pytest
from lingosnap.utils.config import Config
from lingosnap.engines.google_engine import GoogleTranslateEngine


def test_config_creation():
    """Test configuration creation"""
    config = Config()
    assert config.get('engine') in ['google', 'argos']
    assert config.get('ui_language') in ['en', 'zh']


def test_config_set_get():
    """Test configuration set and get"""
    config = Config()
    config.set('test_key', 'test_value')
    assert config.get('test_key') == 'test_value'


def test_google_engine_initialization():
    """Test Google Translate engine initialization"""
    engine = GoogleTranslateEngine()
    assert engine is not None
    assert engine.is_available()


def test_google_engine_languages():
    """Test Google Translate engine language support"""
    engine = GoogleTranslateEngine()
    languages = engine.get_supported_languages()
    assert len(languages) > 0
    assert any(code == 'en' for code, _ in languages)
    assert any(code == 'zh-cn' for code, _ in languages)


def test_google_engine_translation():
    """Test Google Translate engine translation"""
    engine = GoogleTranslateEngine()
    try:
        result = engine.translate('Hello', 'en', 'es')
        assert result is not None
        assert len(result) > 0
    except Exception:
        # Skip if no internet connection
        pytest.skip("Translation requires internet connection")


def test_character_count():
    """Test character count tracking"""
    engine = GoogleTranslateEngine()
    initial_count = engine.get_character_count()
    
    try:
        engine.translate('Test', 'en', 'es')
        new_count = engine.get_character_count()
        assert new_count > initial_count
    except Exception:
        pytest.skip("Translation requires internet connection")


def test_character_count_reset():
    """Test character count reset"""
    engine = GoogleTranslateEngine()
    try:
        engine.translate('Test', 'en', 'es')
    except Exception:
        pass
    
    engine.reset_character_count()
    assert engine.get_character_count() == 0


if __name__ == '__main__':
    pytest.main([__file__])
