import os
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(logs_dir, exist_ok=True)

# Configure default logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

class WhatsAppLogger:
    """Logger class for WhatsApp message routing"""
    
    def __init__(self, log_file: Optional[str] = None):
        """Initialize the logger
        
        Args:
            log_file: Optional path to the log file. If not provided, a default path will be used.
        """
        if log_file is None:
            # Create a log file with the current date
            current_date = datetime.now().strftime("%Y-%m-%d")
            log_file = os.path.join(logs_dir, f"whatsapp_routing_{current_date}.log")
        
        # Create a logger
        self.logger = logging.getLogger("whatsapp_routing")
        self.logger.setLevel(logging.INFO)
        
        # Create a file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # Add the file handler to the logger
        self.logger.addHandler(file_handler)
    
    def log_incoming_message(self, phone_number: str, message_text: str, user_id: Optional[str] = None) -> None:
        """Log an incoming WhatsApp message
        
        Args:
            phone_number: The phone number of the sender
            message_text: The text of the message
            user_id: Optional user ID
        """
        log_data = {
            "event_type": "incoming_message",
            "phone_number": phone_number,
            "message_text": message_text,
            "user_id": user_id or f"whatsapp-{phone_number}",
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(f"INCOMING: {json.dumps(log_data, ensure_ascii=False)}")
    
    def log_parsed_result(self, parsed_result: Dict[str, Any], user_id: Optional[str] = None) -> None:
        """Log a parsed command result
        
        Args:
            parsed_result: The parsed command result
            user_id: Optional user ID
        """
        log_data = {
            "event_type": "parsed_result",
            "intent": parsed_result.get("intent"),
            "entities": parsed_result.get("entities"),
            "language": parsed_result.get("language"),
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(f"PARSED: {json.dumps(log_data, ensure_ascii=False)}")
    
    def log_route_command(self, parsed_result: Dict[str, Any], user_id: Optional[str] = None) -> None:
        """Log a route_command call
        
        Args:
            parsed_result: The parsed command result
            user_id: Optional user ID
        """
        log_data = {
            "event_type": "route_command",
            "intent": parsed_result.get("intent"),
            "entities": parsed_result.get("entities"),
            "language": parsed_result.get("language"),
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(f"ROUTE: {json.dumps(log_data, ensure_ascii=False)}")
    
    def log_outgoing_message(self, phone_number: str, message_text: str, user_id: Optional[str] = None) -> None:
        """Log an outgoing WhatsApp message
        
        Args:
            phone_number: The phone number of the recipient
            message_text: The text of the message
            user_id: Optional user ID
        """
        log_data = {
            "event_type": "outgoing_message",
            "phone_number": phone_number,
            "message_text": message_text,
            "user_id": user_id or f"whatsapp-{phone_number}",
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(f"OUTGOING: {json.dumps(log_data, ensure_ascii=False)}")
    
    def log_error(self, error_message: str, error_type: str, user_id: Optional[str] = None) -> None:
        """Log an error
        
        Args:
            error_message: The error message
            error_type: The type of error
            user_id: Optional user ID
        """
        log_data = {
            "event_type": "error",
            "error_message": error_message,
            "error_type": error_type,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.error(f"ERROR: {json.dumps(log_data, ensure_ascii=False)}")
    
    def log_api_call(self, api_endpoint: str, request_data: Dict[str, Any], response_data: Dict[str, Any], user_id: Optional[str] = None) -> None:
        """Log an API call
        
        Args:
            api_endpoint: The API endpoint
            request_data: The request data
            response_data: The response data
            user_id: Optional user ID
        """
        log_data = {
            "event_type": "api_call",
            "api_endpoint": api_endpoint,
            "request_data": request_data,
            "response_data": response_data,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(f"API: {json.dumps(log_data, ensure_ascii=False)}")

# Create a default logger instance
whatsapp_logger = WhatsAppLogger()

# Export the logger instance
__all__ = ["WhatsAppLogger", "whatsapp_logger"]