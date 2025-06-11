"""
Logging utilities for TEC AI agents.
Provides centralized logging configuration for all agents.
"""
import logging
import os
import sys
from pathlib import Path
from datetime import datetime

def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Get a configured logger for an agent.
    
    Args:
        name: Name of the logger (usually the agent name)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Set logging level
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)
    
    # Create logs directory if it doesn't exist
    logs_dir = Path(__file__).parent.parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    simple_formatter = logging.Formatter(
        '%(levelname)s - %(name)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler for detailed logs
    log_file = logs_dir / f"{name.lower()}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    # System-wide log file
    system_log = logs_dir / "tec_system.log"
    system_handler = logging.FileHandler(system_log)
    system_handler.setLevel(logging.INFO)
    system_handler.setFormatter(detailed_formatter)
    logger.addHandler(system_handler)
    
    return logger

def setup_system_logging():
    """Set up system-wide logging configuration."""
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(
                Path(__file__).parent.parent.parent / "logs" / "system.log"
            )
        ]
    )

# Set up system logging on import
setup_system_logging()
