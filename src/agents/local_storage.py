"""
Local Storage integration for The Elidoras Codex.
Handles storage and retrieval of files using local file system instead of cloud services.
"""
import os
import logging
from typing import Dict, Any, Optional, BinaryIO
from datetime import datetime
import json
import shutil

from .base_agent import BaseAgent

class LocalStorageAgent(BaseAgent):
    """
    LocalStorageAgent handles interactions with the local file system.
    It uploads, downloads, and manages files locally without cloud dependencies.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        super().__init__("LocalStorageAgent", config_path)
        self.logger.info("LocalStorageAgent initialized")
        
        # Initialize storage folder
        self.storage_dir = os.getenv("LOCAL_STORAGE_DIR", os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "storage"))
        
        # Create storage directory if it doesn't exist
        os.makedirs(self.storage_dir, exist_ok=True)
        os.makedirs(os.path.join(self.storage_dir, "backups"), exist_ok=True)
        
        self.logger.info(f"Local storage initialized at: {self.storage_dir}")
    
    def upload_file(self, file_path: str, destination_blob_name: Optional[str] = None) -> Dict[str, Any]:
        """
        "Upload" (copy) a file to local storage.
        
        Args:
            file_path: Path to the local file
            destination_blob_name: Name to save the file as (if None, uses file name)
            
        Returns:
            Dictionary with upload status and path
        """
        try:
            # If no destination name provided, use the file name
            if not destination_blob_name:
                destination_blob_name = os.path.basename(file_path)
            
            # Destination path
            destination_path = os.path.join(self.storage_dir, destination_blob_name)
            
            # Create directories if they don't exist
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            
            # Copy the file
            shutil.copy2(file_path, destination_path)
            
            self.logger.info(f"File {file_path} copied to {destination_path}")
            return {
                "success": True,
                "path": destination_path,
                "blob_name": destination_blob_name
            }
            
        except Exception as e:
            self.logger.error(f"Failed to copy file {file_path}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def download_file(self, blob_name: str, destination_file_path: str) -> Dict[str, Any]:
        """
        "Download" (copy) a file from local storage.
        
        Args:
            blob_name: Name of the file in storage
            destination_file_path: Local path to save the file
            
        Returns:
            Dictionary with download status
        """
        try:
            # Source path
            source_path = os.path.join(self.storage_dir, blob_name)
            
            # Create destination directory if it doesn't exist
            os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
            
            # Copy the file
            shutil.copy2(source_path, destination_file_path)
            
            self.logger.info(f"File {source_path} copied to {destination_file_path}")
            return {
                "success": True,
                "file_path": destination_file_path
            }
            
        except Exception as e:
            self.logger.error(f"Failed to copy file {blob_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def list_files(self, prefix: str = "") -> Dict[str, Any]:
        """
        List files in the storage directory.
        
        Args:
            prefix: Optional prefix to filter files
            
        Returns:
            Dictionary with list of files
        """
        try:
            # Get the full path
            full_path = os.path.join(self.storage_dir, prefix)
            
            # List all files
            files = []
            for root, _, filenames in os.walk(full_path):
                for filename in filenames:
                    # Get the relative path from the storage directory
                    full_file_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(full_file_path, self.storage_dir)
                    
                    # Get file stats
                    stat = os.stat(full_file_path)
                    
                    files.append({
                        "name": rel_path,
                        "size": stat.st_size,
                        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "updated": datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
            
            self.logger.info(f"Listed {len(files)} files in {prefix}")
            return {
                "success": True,
                "files": files
            }
            
        except Exception as e:
            self.logger.error(f"Failed to list files: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def delete_file(self, blob_name: str) -> Dict[str, Any]:
        """
        Delete a file from storage.
        
        Args:
            blob_name: Name of the file to delete
            
        Returns:
            Dictionary with deletion status
        """
        try:
            # Source path
            source_path = os.path.join(self.storage_dir, blob_name)
            
            # Check if it exists
            if not os.path.exists(source_path):
                self.logger.error(f"File {blob_name} not found")
                return {
                    "success": False,
                    "error": f"File {blob_name} not found"
                }
            
            # Delete the file
            os.remove(source_path)
            
            self.logger.info(f"Deleted file {source_path}")
            return {
                "success": True,
                "file": blob_name
            }
            
        except Exception as e:
            self.logger.error(f"Failed to delete file {blob_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def backup_file(self, blob_name: str) -> Dict[str, Any]:
        """
        Backup a file to the backups directory.
        
        Args:
            blob_name: Name of the file to backup
            
        Returns:
            Dictionary with backup status
        """
        try:
            # Source path
            source_path = os.path.join(self.storage_dir, blob_name)
            
            # Check if it exists
            if not os.path.exists(source_path):
                self.logger.error(f"File {blob_name} not found")
                return {
                    "success": False,
                    "error": f"File {blob_name} not found"
                }
            
            # Generate backup name with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{os.path.splitext(blob_name)[0]}_{timestamp}{os.path.splitext(blob_name)[1]}"
            backup_path = os.path.join(self.storage_dir, "backups", backup_name)
            
            # Create backup directories if they don't exist
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            
            # Copy the file
            shutil.copy2(source_path, backup_path)
            
            self.logger.info(f"Backed up {source_path} to {backup_path}")
            return {
                "success": True,
                "original": blob_name,
                "backup": backup_name
            }
            
        except Exception as e:
            self.logger.error(f"Failed to backup file {blob_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def run(self) -> Dict[str, Any]:
        """
        Run a test of the local storage agent.
        
        Returns:
            Dictionary with the test results
        """
        # Create a test file
        test_file_path = os.path.join(self.storage_dir, "test_file.txt")
        with open(test_file_path, "w") as f:
            f.write(f"Test file created at {datetime.now().isoformat()}")
        
        # Test the storage operations
        upload_result = self.upload_file(test_file_path, "test/test_upload.txt")
        list_result = self.list_files()
        backup_result = self.backup_file("test/test_upload.txt")
        delete_result = self.delete_file("test/test_upload.txt")
        
        return {
            "success": True,
            "storage_dir": self.storage_dir,
            "operations": {
                "upload": upload_result,
                "list": list_result,
                "backup": backup_result,
                "delete": delete_result
            }
        }


# For testing the agent standalone
if __name__ == "__main__":
    storage_agent = LocalStorageAgent()
    result = storage_agent.run()
    print(json.dumps(result, indent=2))
