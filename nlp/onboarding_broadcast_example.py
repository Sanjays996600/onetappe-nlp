#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
One Tappe WhatsApp Onboarding Broadcast Example

This script demonstrates how to use the WhatsApp onboarding broadcast templates
to create personalized invitation messages for new sellers.
"""

import json
import os
from datetime import datetime, timedelta
import pandas as pd

class OnboardingBroadcaster:
    """Class to manage WhatsApp onboarding broadcasts."""
    
    def __init__(self, templates_file):
        """Initialize with the path to the templates JSON file."""
        self.templates_file = templates_file
        self.templates = self._load_templates()
    
    def _load_templates(self):
        """Load the broadcast templates from the JSON file."""
        try:
            with open(self.templates_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found at {self.templates_file}")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {self.templates_file}")
            return {}
    
    def create_broadcast_sequence(self, seller_info, language='en'):
        """Create a personalized broadcast sequence for a seller."""
        if not self.templates:
            return []
        
        # Default to English if requested language is not available
        if language not in ['en', 'hi']:
            language = 'en'
        
        # Get the templates
        try:
            initial_invitation = self.templates['onboarding_broadcasts']['initial_invitation'][language]
            feature_highlight = self.templates['onboarding_broadcasts']['feature_highlight'][language]
            action_required = self.templates['onboarding_broadcasts']['action_required'][language]
        except KeyError:
            print("Error: Required templates not found in the JSON file")
            return []
        
        # Personalize the templates
        personalized_invitation = initial_invitation.replace('[Seller Name]', seller_info['name'])
        
        # Create the sequence with recommended send times
        now = datetime.now()
        day1 = now.replace(hour=10, minute=0, second=0, microsecond=0)
        day1_afternoon = now.replace(hour=15, minute=0, second=0, microsecond=0)
        day2 = (now + timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)
        
        sequence = [
            {
                'message': personalized_invitation,
                'scheduled_time': day1.strftime("%Y-%m-%d %H:%M:%S"),
                'type': 'initial_invitation'
            },
            {
                'message': feature_highlight,
                'scheduled_time': day1_afternoon.strftime("%Y-%m-%d %H:%M:%S"),
                'type': 'feature_highlight'
            },
            {
                'message': action_required,
                'scheduled_time': day2.strftime("%Y-%m-%d %H:%M:%S"),
                'type': 'action_required'
            }
        ]
        
        return sequence
    
    def create_batch_broadcasts(self, sellers_csv, language_column='language_preference'):
        """Create broadcast sequences for a batch of sellers from a CSV file."""
        try:
            # Read the sellers CSV
            sellers_df = pd.read_csv(sellers_csv)
            
            # Create a broadcast plan
            broadcast_plan = []
            
            for _, seller in sellers_df.iterrows():
                # Determine language preference
                language = 'en'  # Default
                if language_column in sellers_df.columns:
                    language = seller[language_column] if seller[language_column] in ['en', 'hi'] else 'en'
                
                # Create seller info dict
                seller_info = {
                    'name': seller['name'],
                    'phone': seller['phone'],
                    'business_type': seller.get('business_type', 'retail')
                }
                
                # Create sequence
                sequence = self.create_broadcast_sequence(seller_info, language)
                
                # Add to plan
                broadcast_plan.append({
                    'seller': seller_info,
                    'sequence': sequence
                })
            
            return broadcast_plan
            
        except Exception as e:
            print(f"Error creating batch broadcasts: {e}")
            return []
    
    def export_broadcast_plan(self, broadcast_plan, output_file):
        """Export the broadcast plan to a CSV file for scheduling."""
        # Flatten the broadcast plan for CSV export
        rows = []
        for plan in broadcast_plan:
            seller = plan['seller']
            for message in plan['sequence']:
                rows.append({
                    'phone': seller['phone'],
                    'name': seller['name'],
                    'business_type': seller.get('business_type', ''),
                    'message_type': message['type'],
                    'scheduled_time': message['scheduled_time'],
                    'message': message['message']
                })
        
        # Create DataFrame and export
        df = pd.DataFrame(rows)
        df.to_csv(output_file, index=False)
        print(f"Broadcast plan exported to {output_file}")

# Example usage
def main():
    # Path to the templates file
    templates_file = "whatsapp_onboarding_broadcast_templates.json"
    
    # Check if file exists in current directory, if not, use absolute path
    if not os.path.exists(templates_file):
        templates_file = "/Users/sanjaysuman/One Tappe/OneTappeProject/nlp/whatsapp_onboarding_broadcast_templates.json"
    
    # Initialize the broadcaster
    broadcaster = OnboardingBroadcaster(templates_file)
    
    # Example 1: Create a broadcast sequence for a single seller
    print("\n=== Creating broadcast sequence for a single seller ===\n")
    seller_info = {
        'name': 'Sharma General Store',
        'phone': '+919876543210',
        'business_type': 'retail'
    }
    
    sequence = broadcaster.create_broadcast_sequence(seller_info, 'en')
    
    print(f"Created {len(sequence)} messages for {seller_info['name']}:")
    for i, message in enumerate(sequence, 1):
        print(f"\nMessage {i} ({message['type']})")
        print(f"Scheduled for: {message['scheduled_time']}")
        print(f"Content:\n{message['message']}")
    
    # Example 2: Create a sample sellers CSV for batch processing
    sample_csv = "sample_sellers.csv"
    sample_data = {
        'name': ['Sharma General Store', 'Kumar Electronics', 'Singh Groceries', 'Patel Fashion'],
        'phone': ['+919876543210', '+918765432109', '+917654321098', '+916543210987'],
        'business_type': ['retail', 'electronics', 'grocery', 'clothing'],
        'language_preference': ['en', 'hi', 'hi', 'en']
    }
    
    pd.DataFrame(sample_data).to_csv(sample_csv, index=False)
    print(f"\nCreated sample sellers CSV at {sample_csv}")
    
    # Example 3: Create batch broadcasts
    print("\n=== Creating batch broadcasts ===\n")
    broadcast_plan = broadcaster.create_batch_broadcasts(sample_csv)
    print(f"Created broadcast plan for {len(broadcast_plan)} sellers")
    
    # Example 4: Export the broadcast plan
    output_file = "broadcast_schedule.csv"
    broadcaster.export_broadcast_plan(broadcast_plan, output_file)
    
    # Clean up sample file
    os.remove(sample_csv)

# Run the example if script is executed directly
if __name__ == "__main__":
    main()