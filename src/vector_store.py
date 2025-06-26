"""
Legacy Memory Assistant - Vector Store
Handles semantic search and indexing of memories using embeddings.
"""

import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import uuid
from typing import List, Dict, Optional, Tuple
import json
import os
from datetime import datetime


class VectorMemoryStore:
    """Manages semantic search and storage of memories using vector embeddings."""
    
    def __init__(self, collection_name: str = "memories", model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the vector store.
        
        Args:
            collection_name: Name of the ChromaDB collection
            model_name: Sentence transformer model name
        """
        self.collection_name = collection_name
        self.model_name = model_name
        
        # Initialize embedding model
        print(f"Loading embedding model: {model_name}")
        self.embedding_model = SentenceTransformer(model_name)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path="./memory_vectors",
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Create or get collection
        try:
            self.collection = self.client.get_collection(collection_name)
            print(f"Loaded existing collection: {collection_name}")
        except ValueError:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"description": "Personal memory embeddings"}
            )
            print(f"Created new collection: {collection_name}")
    
    def add_memory(self, memory_id: str, content: str, metadata: Dict = None) -> str:
        """
        Add a memory to the vector store.
        
        Args:
            memory_id: Unique identifier for the memory
            content: Memory content text
            metadata: Additional metadata
            
        Returns:
            Vector store ID for the memory
        """
        if not content or not content.strip():
            raise ValueError("Memory content cannot be empty")
        
        # Generate embedding
        embedding = self.embedding_model.encode(content).tolist()
        
        # Prepare metadata
        meta = metadata or {}
        meta.update({
            'memory_id': memory_id,
            'content_length': len(content),
            'added_at': datetime.now().isoformat(),
            'content_preview': content[:100] + "..." if len(content) > 100 else content
        })
        
        # Generate unique vector ID
        vector_id = str(uuid.uuid4())
        
        try:
            # Add to collection
            self.collection.add(
                ids=[vector_id],
                embeddings=[embedding],
                documents=[content],
                metadatas=[meta]
            )
            
            print(f"Added memory to vector store: {memory_id}")
            return vector_id
            
        except Exception as e:
            print(f"Error adding memory to vector store: {e}")
            raise
    
    def search_memories(self, query: str, n_results: int = 10, 
                       similarity_threshold: float = 0.5) -> List[Dict]:
        """
        Search for memories using semantic similarity.
        
        Args:
            query: Search query text
            n_results: Maximum number of results to return
            similarity_threshold: Minimum similarity score (0-1)
            
        Returns:
            List of matching memories with similarity scores
        """
        if not query or not query.strip():
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Search in collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=['documents', 'metadatas', 'distances']
            )
            
            # Process results
            memories = []
            if results['ids'] and results['ids'][0]:
                for i, doc_id in enumerate(results['ids'][0]):
                    # Convert distance to similarity score (ChromaDB uses cosine distance)
                    distance = results['distances'][0][i]
                    similarity = 1 - distance  # Convert distance to similarity
                    
                    if similarity >= similarity_threshold:
                        memory = {
                            'vector_id': doc_id,
                            'content': results['documents'][0][i],
                            'metadata': results['metadatas'][0][i],
                            'similarity_score': similarity,
                            'memory_id': results['metadatas'][0][i].get('memory_id', 'unknown')
                        }
                        memories.append(memory)
            
            # Sort by similarity score (highest first)
            memories.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            print(f"Found {len(memories)} memories for query: '{query}'")
            return memories
            
        except Exception as e:
            print(f"Error searching memories: {e}")
            return []
    
    def get_similar_memories(self, memory_id: str, n_results: int = 5) -> List[Dict]:
        """
        Find memories similar to a given memory.
        
        Args:
            memory_id: ID of the reference memory
            n_results: Number of similar memories to return
            
        Returns:
            List of similar memories
        """
        try:
            # Get the reference memory
            results = self.collection.get(
                where={"memory_id": memory_id},
                include=['documents', 'metadatas']
            )
            
            if not results['ids']:
                print(f"Memory not found: {memory_id}")
                return []
            
            # Use the first matching document for similarity search
            reference_content = results['documents'][0]
            return self.search_memories(reference_content, n_results + 1)[1:]  # Exclude self
            
        except Exception as e:
            print(f"Error finding similar memories: {e}")
            return []
    
    def get_memory_clusters(self, n_clusters: int = 5) -> Dict[str, List[Dict]]:
        """
        Group memories into thematic clusters.
        
        Args:
            n_clusters: Number of clusters to create
            
        Returns:
            Dictionary mapping cluster names to memories
        """
        try:
            # Get all memories
            all_memories = self.collection.get(include=['documents', 'metadatas', 'embeddings'])
            
            if not all_memories['ids']:
                return {}
            
            # Perform clustering (simplified approach)
            from sklearn.cluster import KMeans
            
            embeddings = np.array(all_memories['embeddings'])
            kmeans = KMeans(n_clusters=min(n_clusters, len(embeddings)), random_state=42)
            cluster_labels = kmeans.fit_predict(embeddings)
            
            # Group memories by cluster
            clusters = {}
            for i, (doc_id, content, metadata) in enumerate(zip(
                all_memories['ids'], 
                all_memories['documents'], 
                all_memories['metadatas']
            )):
                cluster_id = f"cluster_{cluster_labels[i]}"
                if cluster_id not in clusters:
                    clusters[cluster_id] = []
                
                clusters[cluster_id].append({
                    'vector_id': doc_id,
                    'content': content,
                    'metadata': metadata,
                    'memory_id': metadata.get('memory_id', 'unknown')
                })
            
            return clusters
            
        except ImportError:
            print("scikit-learn not installed. Cannot perform clustering.")
            return {}
        except Exception as e:
            print(f"Error clustering memories: {e}")
            return {}
    
    def delete_memory(self, memory_id: str) -> bool:
        """
        Delete a memory from the vector store.
        
        Args:
            memory_id: Memory ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        try:
            # Find the vector ID for this memory
            results = self.collection.get(
                where={"memory_id": memory_id},
                include=['metadatas']
            )
            
            if not results['ids']:
                print(f"Memory not found in vector store: {memory_id}")
                return False
            
            # Delete all vectors for this memory
            self.collection.delete(ids=results['ids'])
            print(f"Deleted memory from vector store: {memory_id}")
            return True
            
        except Exception as e:
            print(f"Error deleting memory from vector store: {e}")
            return False
    
    def get_store_stats(self) -> Dict:
        """Get statistics about the vector store."""
        try:
            all_memories = self.collection.get(include=['metadatas'])
            
            total_count = len(all_memories['ids'])
            
            # Analyze metadata
            emotions = {}
            tags = {}
            
            for metadata in all_memories['metadatas']:
                # Count emotions
                emotion = metadata.get('emotion', 'unknown')
                emotions[emotion] = emotions.get(emotion, 0) + 1
                
                # Count tags
                memory_tags = metadata.get('tags', [])
                if isinstance(memory_tags, str):
                    memory_tags = json.loads(memory_tags)
                
                for tag in memory_tags:
                    tags[tag] = tags.get(tag, 0) + 1
            
            return {
                'total_memories': total_count,
                'collection_name': self.collection_name,
                'model_name': self.model_name,
                'emotions': emotions,
                'tags': tags
            }
            
        except Exception as e:
            print(f"Error getting store stats: {e}")
            return {'error': str(e)}
    
    def export_embeddings(self, output_path: str):
        """
        Export embeddings and metadata to a file.
        
        Args:
            output_path: Path to save the export
        """
        try:
            all_data = self.collection.get(
                include=['documents', 'metadatas', 'embeddings']
            )
            
            export_data = {
                'collection_name': self.collection_name,
                'model_name': self.model_name,
                'export_date': datetime.now().isoformat(),
                'memories': []
            }
            
            for i, doc_id in enumerate(all_data['ids']):
                export_data['memories'].append({
                    'vector_id': doc_id,
                    'content': all_data['documents'][i],
                    'metadata': all_data['metadatas'][i],
                    'embedding': all_data['embeddings'][i]
                })
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            print(f"Exported {len(export_data['memories'])} memories to {output_path}")
            
        except Exception as e:
            print(f"Error exporting embeddings: {e}")
    
    def reset_store(self):
        """Reset the vector store (delete all data)."""
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Personal memory embeddings"}
            )
            print(f"Reset vector store: {self.collection_name}")
        except Exception as e:
            print(f"Error resetting store: {e}")


class SemanticMemorySearch:
    """High-level interface for semantic memory search."""
    
    def __init__(self, vector_store: VectorMemoryStore):
        """
        Initialize semantic search.
        
        Args:
            vector_store: Vector store instance
        """
        self.vector_store = vector_store
    
    def find_memories_about(self, topic: str, limit: int = 10) -> List[Dict]:
        """Find memories about a specific topic."""
        return self.vector_store.search_memories(topic, n_results=limit)
    
    def find_emotional_memories(self, emotion: str, limit: int = 10) -> List[Dict]:
        """Find memories with specific emotional content."""
        emotion_queries = {
            'happy': 'joy happiness celebration good times laughter',
            'sad': 'sadness loss grief difficult times',
            'proud': 'achievement success accomplishment pride',
            'love': 'love affection caring family relationships',
            'nostalgic': 'memories past times childhood remember'
        }
        
        query = emotion_queries.get(emotion.lower(), emotion)
        return self.vector_store.search_memories(query, n_results=limit)
    
    def find_memories_by_timeframe(self, timeframe: str, limit: int = 10) -> List[Dict]:
        """Find memories from a specific timeframe."""
        timeframe_queries = {
            'childhood': 'childhood young kid child school playground',
            'teenage': 'teenager high school adolescent growing up',
            'young adult': 'college university young adult twenties',
            'recent': 'recent lately nowadays today this year'
        }
        
        query = timeframe_queries.get(timeframe.lower(), timeframe)
        return self.vector_store.search_memories(query, n_results=limit)


if __name__ == "__main__":
    # Example usage
    store = VectorMemoryStore()
    
    # Add sample memories
    sample_memories = [
        {
            'id': 'mem_001',
            'content': 'Today was your first day of school and you were so excited to meet new friends.',
            'metadata': {'emotion': 'happy', 'tags': ['school', 'milestone', 'childhood']}
        },
        {
            'id': 'mem_002', 
            'content': 'We had a wonderful picnic in the park and watched the sunset together.',
            'metadata': {'emotion': 'peaceful', 'tags': ['family', 'nature', 'quality_time']}
        }
    ]
    
    for memory in sample_memories:
        store.add_memory(memory['id'], memory['content'], memory['metadata'])
    
    # Test search
    results = store.search_memories("school and friends", n_results=5)
    print(f"Search results: {len(results)}")
    for result in results:
        print(f"  - {result['content'][:50]}... (similarity: {result['similarity_score']:.3f})")
    
    # Test semantic search
    semantic_search = SemanticMemorySearch(store)
    happy_memories = semantic_search.find_emotional_memories('happy')
    print(f"\nHappy memories: {len(happy_memories)}")
    
    # Get stats
    stats = store.get_store_stats()
    print(f"\nStore stats: {stats}")
