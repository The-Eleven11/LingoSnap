"""
Translation history database management
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class HistoryDatabase:
    """SQLite database for translation history"""
    
    def __init__(self):
        """Initialize history database"""
        self.db_dir = Path.home() / '.lingosnap'
        self.db_file = self.db_dir / 'history.db'
        self._init_database()
    
    def _init_database(self):
        """Create database and tables if they don't exist"""
        try:
            # Create directory if it doesn't exist
            self.db_dir.mkdir(parents=True, exist_ok=True)
            
            # Connect and create table
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    source_lang TEXT NOT NULL,
                    target_lang TEXT NOT NULL,
                    source_text TEXT NOT NULL,
                    translated_text TEXT NOT NULL
                )
            ''')
            
            # Create index on timestamp for faster queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON history(timestamp DESC)
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            raise Exception(f"Failed to initialize database: {str(e)}")
    
    def add_entry(self, source_lang: str, target_lang: str, 
                  source_text: str, translated_text: str):
        """
        Add a translation entry to history
        
        Args:
            source_lang: Source language code
            target_lang: Target language code
            source_text: Original text
            translated_text: Translated text
        """
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            
            timestamp = datetime.now().isoformat()
            
            cursor.execute('''
                INSERT INTO history 
                (timestamp, source_lang, target_lang, source_text, translated_text)
                VALUES (?, ?, ?, ?, ?)
            ''', (timestamp, source_lang, target_lang, source_text, translated_text))
            
            conn.commit()
            conn.close()
        except Exception as e:
            raise Exception(f"Failed to add history entry: {str(e)}")
    
    def get_history(self, limit: int = 100) -> List[Dict]:
        """
        Get translation history
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of history entries
        """
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, timestamp, source_lang, target_lang, 
                       source_text, translated_text
                FROM history
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'id': row[0],
                    'timestamp': row[1],
                    'source_lang': row[2],
                    'target_lang': row[3],
                    'source_text': row[4],
                    'translated_text': row[5]
                }
                for row in rows
            ]
        except Exception:
            return []
    
    def clear_history(self):
        """Clear all history entries"""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            cursor.execute('DELETE FROM history')
            conn.commit()
            conn.close()
        except Exception as e:
            raise Exception(f"Failed to clear history: {str(e)}")
    
    def delete_entry(self, entry_id: int):
        """
        Delete a specific history entry
        
        Args:
            entry_id: ID of the entry to delete
        """
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            cursor.execute('DELETE FROM history WHERE id = ?', (entry_id,))
            conn.commit()
            conn.close()
        except Exception as e:
            raise Exception(f"Failed to delete entry: {str(e)}")
