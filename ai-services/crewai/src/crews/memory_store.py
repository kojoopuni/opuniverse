# src/crews/memory_store.py

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class BaseMemoryStore:
    """Base memory store implementation with common functionality"""
    
    def __init__(self, storage_dir: str = "memory"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.categories = {}  # To be defined by child classes
        
    def _initialize_storage(self):
        """Initialize storage files if they don't exist"""
        for file_path in self.categories.values():
            if not file_path.exists():
                with open(file_path, 'w') as f:
                    json.dump({}, f)

    def _store_data(self, category: str, key: str, data: Dict[str, Any]):
        """Base method for storing data"""
        file_path = self.categories[category]
        try:
            with open(file_path, 'r') as f:
                current_data = json.load(f)
            
            # Store historical data
            if key in current_data:
                if not isinstance(current_data[key], list):
                    current_data[key] = [current_data[key]]
                current_data[key].append(data)
            else:
                current_data[key] = data
            
            with open(file_path, 'w') as f:
                json.dump(current_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error storing data in {category}: {str(e)}")
            raise

    def _get_data(self, category: str, key: str) -> Optional[Dict[str, Any]]:
        """Base method for retrieving data"""
        file_path = self.categories[category]
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data.get(key)
        except Exception as e:
            logger.error(f"Error retrieving data from {category}: {str(e)}")
            return None