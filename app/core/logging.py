import logging
import sys
from typing import Any, Dict
import json
from app.core.config import get_settings

settings = get_settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

def log_event(event_type: str, data: Dict[str, Any]) -> None:
    """Log a structured event."""
    log_entry = {
        "event_type": event_type,
        "data": data
    }
    logger.info(json.dumps(log_entry, default=str))

def log_error(error: Exception, context: Dict[str, Any]) -> None:
    """Log an error with context."""
    log_entry = {
        "error_type": error.__class__.__name__,
        "error_message": str(error),
        "context": context
    }
    logger.error(json.dumps(log_entry, default=str))
