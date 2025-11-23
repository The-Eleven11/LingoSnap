#!/usr/bin/env python3
"""
LingoSnap terminal integration
Command-line tool for translating terminal output
"""

import sys
import argparse
import subprocess
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lingosnap.utils.config import Config
from lingosnap.engines.google_engine import GoogleTranslateEngine
from lingosnap.engines.argos_engine import ArgosTranslateEngine


def get_previous_terminal_output(n: int) -> str:
    """
    Get previous terminal output
    
    This is a challenging feature as standard shells don't easily expose
    previous command output. This implementation uses a simple approach
    that may need improvement based on the specific terminal and shell.
    
    Args:
        n: Number of lines back to capture
        
    Returns:
        Captured text
    """
    # Try to get from history file or shell
    # Note: This is a simplified implementation
    # A more robust solution might require shell integration or tmux
    
    try:
        # Try to read from shell history or screen buffer
        # This is a placeholder - actual implementation depends on terminal type
        
        # For demonstration, we'll use a simple approach with tput
        # In production, this might require terminal-specific solutions
        
        # Try to use tmux if available
        result = subprocess.run(['which', 'tmux'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            # Try to capture from tmux buffer
            result = subprocess.run(['tmux', 'capture-pane', '-p'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                # Get last n lines (excluding the current command)
                if len(lines) > 1:
                    return '\n'.join(lines[-n-1:-1])
        
        # Fallback: prompt user to paste content
        print("Note: Automatic terminal output capture requires tmux or special terminal setup.")
        print(f"Please paste the last {n} line(s) of output and press Ctrl+D:")
        
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
        
        return '\n'.join(lines[-n:])
        
    except Exception as e:
        print(f"Error capturing terminal output: {e}", file=sys.stderr)
        return ""


def main():
    """Main entry point for terminal integration"""
    parser = argparse.ArgumentParser(
        description='LingoSnap Terminal - Translate terminal output',
        epilog='Example: lingo -t 1 -l fr'
    )
    
    parser.add_argument(
        '-t', '--target-line',
        type=int,
        default=1,
        help='Number of previous terminal output lines to translate (default: 1)'
    )
    
    parser.add_argument(
        '-l', '--language',
        type=str,
        help='Target language code (e.g., zh, fr, es). If not specified, uses default from settings.'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = Config()
    
    # Get engine
    engine_type = config.get('engine', 'google')
    if engine_type == 'google':
        engine = GoogleTranslateEngine()
    else:
        engine = ArgosTranslateEngine()
    
    # Check if engine is available
    if not engine.is_available():
        print(f"Error: {engine_type.capitalize()} engine is not available.", 
              file=sys.stderr)
        if engine_type == 'argos':
            print("Please install Argos language packages first.", file=sys.stderr)
        sys.exit(1)
    
    # Get target language
    target_lang = args.language
    if not target_lang:
        target_lang = config.get('terminal_default_target', 'zh')
    
    # Normalize language code for the engine
    # Google uses 'zh-cn', Argos uses 'zh'
    if engine_type == 'google':
        # Convert simplified codes to Google format
        if target_lang == 'zh':
            target_lang = 'zh-cn'
    else:  # argos
        # Convert Google format to simplified codes
        if target_lang == 'zh-cn' or target_lang == 'zh-tw':
            target_lang = 'zh'
    
    # Validate target language
    supported_langs = engine.get_supported_languages()
    lang_codes = [code for code, _ in supported_langs]
    
    if target_lang not in lang_codes:
        print(f"Error: Language '{target_lang}' is not supported by {engine_type} engine.", 
              file=sys.stderr)
        print(f"Supported languages: {', '.join(sorted(set(lang_codes)))}", 
              file=sys.stderr)
        sys.exit(1)
    
    # Get terminal output
    text = get_previous_terminal_output(args.target_line)
    
    if not text or not text.strip():
        print("Error: No text captured from terminal.", file=sys.stderr)
        sys.exit(1)
    
    # Detect source language
    try:
        source_lang = engine.detect_language(text)
        if not source_lang:
            source_lang = 'auto'
    except:
        source_lang = 'auto'
    
    # Translate
    try:
        translated = engine.translate(text, source_lang, target_lang)
        print(translated)
    except Exception as e:
        print(f"Translation failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
