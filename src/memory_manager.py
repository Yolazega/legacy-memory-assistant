"""
Legacy Memory Assistant - Memory Manager
Handles storage, retrieval, and organization of personal memories.
"""

import json
import sqlite3
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from cryptography.fernet import Fernet
import os


class MemoryManager:
    """Manages secure storage and retrieval of personal memories."""
    
    def __init__(self, db_path: str = "memories.db", encryption_key: Optional[bytes] = None):
        """
        Initialize the memory manager.
        
        Args:
            db_path: Path to the SQLite database file
            encryption_key: Optional encryption key for sensitive data
        """
        self.db_path = db_path
        self.encryption_key = encryption_key or self._generate_key()
        self.cipher = Fernet(self.encryption_key)
        self._init_database()
    
    def _generate_key(self) -> bytes:
        """Generate a new encryption key."""
        return Fernet.generate_key()
    
    def _init_database(self):
        """Initialize the SQLite database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create memories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                content_hash TEXT UNIQUE,
                encrypted_content BLOB,
                emotion TEXT,
                tags TEXT,
                metadata TEXT,
                is_private BOOLEAN DEFAULT 1
            )
        ''')
        
        # Create tags table for better organization
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                description TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_memory(self, content: str, emotion: str = "neutral", 
                    tags: List[str] = None, metadata: Dict = None,
                    is_private: bool = True) -> str:
        """
        Store a new memory entry.
        
        Args:
            content: The memory content (text)
            emotion: Detected or specified emotion
            tags: List of tags for categorization
            metadata: Additional metadata (timestamps, location, etc.)
            is_private: Whether this memory is private
            
        Returns:
            Memory ID (hash) of the stored memory
        """
        # Create content hash for deduplication
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        # Encrypt the content
        encrypted_content = self.cipher.encrypt(content.encode())
        
        # Prepare data
        tags_str = json.dumps(tags or [])
        metadata_str = json.dumps(metadata or {})
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO memories (content_hash, encrypted_content, emotion, tags, metadata, is_private)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (content_hash, encrypted_content, emotion, tags_str, metadata_str, is_private))
            
            conn.commit()
            return content_hash
            
        except sqlite3.IntegrityError:
            # Memory already exists
            return content_hash
        finally:
            conn.close()
    
    def retrieve_memory(self, memory_id: str) -> Optional[Dict]:
        """
        Retrieve a specific memory by ID.
        
        Args:
            memory_id: The memory hash ID
            
        Returns:
            Memory data or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM memories WHERE content_hash = ?
        ''', (memory_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._decrypt_memory_row(row)
        return None
    
    def search_memories(self, query: str = None, tags: List[str] = None,
                       emotion: str = None, limit: int = 50) -> List[Dict]:
        """
        Search memories based on various criteria.
        
        Args:
            query: Text search query
            tags: Filter by tags
            emotion: Filter by emotion
            limit: Maximum number of results
            
        Returns:
            List of matching memories
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build dynamic query
        conditions = []
        params = []
        
        if emotion:
            conditions.append("emotion = ?")
            params.append(emotion)
        
        if tags:
            for tag in tags:
                conditions.append("tags LIKE ?")
                params.append(f"%{tag}%")
        
        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
        
        cursor.execute(f'''
            SELECT * FROM memories {where_clause}
            ORDER BY timestamp DESC
            LIMIT ?
        ''', params + [limit])
        
        rows = cursor.fetchall()
        conn.close()
        
        memories = []
        for row in rows:
            memory = self._decrypt_memory_row(row)
            if memory and (not query or query.lower() in memory['content'].lower()):
                memories.append(memory)
        
        return memories
    
    def _decrypt_memory_row(self, row: Tuple) -> Dict:
        """Decrypt and format a memory row from the database."""
        try:
            decrypted_content = self.cipher.decrypt(row[3]).decode()
            
            return {
                'id': row[0],
                'timestamp': row[1],
                'content_hash': row[2],
                'content': decrypted_content,
                'emotion': row[4],
                'tags': json.loads(row[5]),
                'metadata': json.loads(row[6]),
                'is_private': bool(row[7])
            }
        except Exception as e:
            print(f"Error decrypting memory: {e}")
            return None
    
    def delete_memory(self, memory_id: str) -> bool:
        """
        Delete a memory by ID.
        
        Args:
            memory_id: The memory hash ID
            
        Returns:
            True if deleted, False if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM memories WHERE content_hash = ?', (memory_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
    
    def get_memory_stats(self) -> Dict:
        """Get statistics about stored memories."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM memories')
        total_memories = cursor.fetchone()[0]
        
        cursor.execute('SELECT emotion, COUNT(*) FROM memories GROUP BY emotion')
        emotions = dict(cursor.fetchall())
        
        cursor.execute('SELECT DATE(timestamp), COUNT(*) FROM memories GROUP BY DATE(timestamp) ORDER BY DATE(timestamp) DESC LIMIT 30')
        daily_counts = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'total_memories': total_memories,
            'emotions': emotions,
            'daily_counts': daily_counts
        }
    
    def export_memories(self, output_path: str, include_private: bool = False):
        """
        Export memories to a JSON file.
        
        Args:
            output_path: Path to save the export file
            include_private: Whether to include private memories
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = 'SELECT * FROM memories'
        if not include_private:
            query += ' WHERE is_private = 0'
        
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        memories = []
        for row in rows:
            memory = self._decrypt_memory_row(row)
            if memory:
                memories.append(memory)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(memories, f, indent=2, default=str)
        
        print(f"Exported {len(memories)} memories to {output_path}")


if __name__ == "__main__":
    # Example usage
    manager = MemoryManager()
    
    # Store a memory
    memory_id = manager.store_memory(
        content="Today was a wonderful day with my family at the park.",
        emotion="happy",
        tags=["family", "park", "joy"],
        metadata={"location": "Central Park", "weather": "sunny"}
    )
    
    # Retrieve the memory
    memory = manager.retrieve_memory(memory_id)
    print("Retrieved memory:", memory)
    
    # Search memories
    happy_memories = manager.search_memories(emotion="happy")
    print(f"Found {len(happy_memories)} happy memories")
    
    # Get stats
    stats = manager.get_memory_stats()
    print("Memory statistics:", stats)
