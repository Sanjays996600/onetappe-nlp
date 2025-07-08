#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
One Tappe Seller Support Tracker Example

This script demonstrates how to use the seller support tracker CSV
to log and manage support issues from WhatsApp conversations.
"""

import csv
import os
from datetime import datetime
import pandas as pd

class SellerSupportTracker:
    """Class to manage the seller support tracking system."""
    
    # Define constants
    ISSUE_TYPES = ["Bug", "Help", "Feature Request", "Complaint"]
    STATUS_TYPES = ["Pending", "In Progress", "Resolved", "Escalated", "Awaiting Seller Response"]
    
    def __init__(self, csv_path):
        """Initialize the tracker with the path to the CSV file."""
        self.csv_path = csv_path
        self.headers = [
            "WhatsApp Number", 
            "Seller Name", 
            "Issue Type", 
            "Description", 
            "Status", 
            "Assigned To", 
            "Resolution Summary", 
            "Timestamp"
        ]
        
        # Create the CSV file if it doesn't exist
        if not os.path.exists(csv_path):
            self._create_new_tracker()
    
    def _create_new_tracker(self):
        """Create a new tracker CSV file with headers."""
        with open(self.csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.headers)
    
    def add_issue(self, whatsapp_number, seller_name, issue_type, description, 
                  assigned_to="Unassigned", status="Pending", resolution_summary=""):
        """Add a new issue to the tracker."""
        # Validate issue type
        if issue_type not in self.ISSUE_TYPES:
            raise ValueError(f"Issue type must be one of: {', '.join(self.ISSUE_TYPES)}")
        
        # Validate status
        if status not in self.STATUS_TYPES:
            raise ValueError(f"Status must be one of: {', '.join(self.STATUS_TYPES)}")
        
        # Create timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Add the new issue
        with open(self.csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                whatsapp_number,
                seller_name,
                issue_type,
                description,
                status,
                assigned_to,
                resolution_summary,
                timestamp
            ])
        
        return timestamp  # Return the timestamp for reference
    
    def update_issue(self, whatsapp_number, timestamp, **kwargs):
        """Update an existing issue identified by WhatsApp number and timestamp."""
        # Read the entire CSV
        df = pd.read_csv(self.csv_path)
        
        # Find the matching row
        mask = (df['WhatsApp Number'] == whatsapp_number) & (df['Timestamp'] == timestamp)
        if not any(mask):
            raise ValueError(f"No issue found for {whatsapp_number} at {timestamp}")
        
        # Update the specified fields
        for key, value in kwargs.items():
            if key in df.columns:
                # Validate issue type and status if they're being updated
                if key == "Issue Type" and value not in self.ISSUE_TYPES:
                    raise ValueError(f"Issue type must be one of: {', '.join(self.ISSUE_TYPES)}")
                if key == "Status" and value not in self.STATUS_TYPES:
                    raise ValueError(f"Status must be one of: {', '.join(self.STATUS_TYPES)}")
                
                df.loc[mask, key] = value
            else:
                raise ValueError(f"Invalid field: {key}")
        
        # Write back to CSV
        df.to_csv(self.csv_path, index=False)
    
    def get_issues_by_seller(self, whatsapp_number):
        """Get all issues for a specific seller."""
        df = pd.read_csv(self.csv_path)
        return df[df['WhatsApp Number'] == whatsapp_number].to_dict('records')
    
    def get_issues_by_status(self, status):
        """Get all issues with a specific status."""
        if status not in self.STATUS_TYPES:
            raise ValueError(f"Status must be one of: {', '.join(self.STATUS_TYPES)}")
        
        df = pd.read_csv(self.csv_path)
        return df[df['Status'] == status].to_dict('records')
    
    def get_issues_by_type(self, issue_type):
        """Get all issues of a specific type."""
        if issue_type not in self.ISSUE_TYPES:
            raise ValueError(f"Issue type must be one of: {', '.join(self.ISSUE_TYPES)}")
        
        df = pd.read_csv(self.csv_path)
        return df[df['Issue Type'] == issue_type].to_dict('records')
    
    def get_issues_by_assignee(self, assigned_to):
        """Get all issues assigned to a specific person."""
        df = pd.read_csv(self.csv_path)
        return df[df['Assigned To'] == assigned_to].to_dict('records')
    
    def get_all_issues(self):
        """Get all issues in the tracker."""
        df = pd.read_csv(self.csv_path)
        return df.to_dict('records')
    
    def generate_daily_summary(self):
        """Generate a summary of issues for the current day."""
        df = pd.read_csv(self.csv_path)
        
        # Get today's date
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Filter for today's issues
        today_df = df[df['Timestamp'].str.startswith(today)]
        
        # Generate summary
        summary = {
            "total_issues": len(today_df),
            "by_status": today_df['Status'].value_counts().to_dict(),
            "by_type": today_df['Issue Type'].value_counts().to_dict(),
            "by_assignee": today_df['Assigned To'].value_counts().to_dict(),
            "resolved_count": len(today_df[today_df['Status'] == 'Resolved']),
            "pending_count": len(today_df[today_df['Status'] == 'Pending']),
            "escalated_count": len(today_df[today_df['Status'] == 'Escalated'])
        }
        
        return summary

# Example usage
def main():
    # Path to the tracker CSV
    tracker_file = "seller_support_tracker.csv"
    
    # Check if file exists in current directory, if not, use absolute path
    if not os.path.exists(tracker_file):
        tracker_file = "/Users/sanjaysuman/One Tappe/OneTappeProject/nlp/seller_support_tracker.csv"
    
    # Initialize the tracker
    tracker = SellerSupportTracker(tracker_file)
    
    # Example 1: Add a new issue
    print("\n=== Adding a new support issue ===\n")
    timestamp = tracker.add_issue(
        whatsapp_number="+919876543210",
        seller_name="Sharma General Store",
        issue_type="Help",
        description="Unable to understand how to add multiple products at once",
        assigned_to="Priya",
        status="Pending"
    )
    print(f"Issue added with timestamp: {timestamp}")
    
    # Example 2: Add another issue
    print("\n=== Adding another support issue ===\n")
    bug_timestamp = tracker.add_issue(
        whatsapp_number="+918765432109",
        seller_name="Kumar Electronics",
        issue_type="Bug",
        description="Getting 'Product not found' error when searching for 'Mobile Charger' even though it exists in inventory",
        assigned_to="Rahul",
        status="Escalated"
    )
    print(f"Bug issue added with timestamp: {bug_timestamp}")
    
    # Example 3: Update an issue
    print("\n=== Updating a support issue ===\n")
    try:
        tracker.update_issue(
            whatsapp_number="+919876543210",
            timestamp=timestamp,
            Status="Resolved",
            Resolution_Summary="Explained that multiple products need to be added one by one currently. Feature request noted for batch upload."
        )
        print("Issue updated successfully")
    except ValueError as e:
        print(f"Error: {e}")
    
    # Example 4: Get issues by seller
    print("\n=== Getting issues for a specific seller ===\n")
    seller_issues = tracker.get_issues_by_seller("+919876543210")
    for issue in seller_issues:
        print(f"Issue: {issue['Description']}")
        print(f"Status: {issue['Status']}")
        print(f"Resolution: {issue['Resolution Summary']}")
    
    # Example 5: Generate daily summary
    print("\n=== Generating daily summary ===\n")
    summary = tracker.generate_daily_summary()
    print(f"Total issues today: {summary['total_issues']}")
    print(f"Issues by status: {summary['by_status']}")
    print(f"Issues by type: {summary['by_type']}")
    print(f"Resolved issues: {summary['resolved_count']}")
    print(f"Pending issues: {summary['pending_count']}")
    print(f"Escalated issues: {summary['escalated_count']}")

# Run the example if script is executed directly
if __name__ == "__main__":
    main()