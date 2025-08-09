"""
Sample Python code for testing CodeForge AI
This file contains various code patterns to test the analysis capabilities
"""

import os
import sys
from typing import List, Dict, Optional
import json
import requests
from datetime import datetime


class UserManager:
    """A simple user management system with some issues for testing"""
    
    def __init__(self):
        self.users = {}
        self.user_count = 0
    
    def add_user(self, username: str, email: str, password: str) -> bool:
        """Add a new user to the system"""
        if username in self.users:
            return False
        
        # Security issue: storing password in plain text
        user_data = {
            'username': username,
            'email': email,
            'password': password,  # Should be hashed!
            'created_at': datetime.now().isoformat()
        }
        
        self.users[username] = user_data
        self.user_count += 1
        return True
    
    def get_user(self, username: str) -> Optional[Dict]:
        """Get user information"""
        return self.users.get(username)
    
    def update_user(self, username: str, **kwargs) -> bool:
        """Update user information"""
        if username not in self.users:
            return False
        
        # Performance issue: inefficient nested loops
        for key, value in kwargs.items():
            for user_key in self.users[username]:
                if key == user_key:
                    self.users[username][key] = value
                    break
        
        return True
    
    def delete_user(self, username: str) -> bool:
        """Delete a user"""
        if username in self.users:
            del self.users[username]
            self.user_count -= 1
            return True
        return False
    
    def list_users(self) -> List[Dict]:
        """List all users"""
        return list(self.users.values())


class DataProcessor:
    """A data processing class with some complexity issues"""
    
    def __init__(self):
        self.data = []
        self.processed_data = []
    
    def add_data(self, item: Dict) -> None:
        """Add data item"""
        self.data.append(item)
    
    def process_data(self) -> List[Dict]:
        """Process all data items"""
        # Complexity issue: deeply nested logic
        for item in self.data:
            if item.get('type') == 'user':
                if item.get('status') == 'active':
                    if item.get('age', 0) > 18:
                        if item.get('verified', False):
                            processed_item = {
                                'id': item.get('id'),
                                'name': item.get('name'),
                                'processed': True,
                                'timestamp': datetime.now().isoformat()
                            }
                            self.processed_data.append(processed_item)
                        else:
                            # Handle unverified users
                            processed_item = {
                                'id': item.get('id'),
                                'name': item.get('name'),
                                'processed': False,
                                'reason': 'unverified',
                                'timestamp': datetime.now().isoformat()
                            }
                            self.processed_data.append(processed_item)
                    else:
                        # Handle underage users
                        processed_item = {
                            'id': item.get('id'),
                            'name': item.get('name'),
                            'processed': False,
                            'reason': 'underage',
                            'timestamp': datetime.now().isoformat()
                        }
                        self.processed_data.append(processed_item)
                else:
                    # Handle inactive users
                    processed_item = {
                        'id': item.get('id'),
                        'name': item.get('name'),
                        'processed': False,
                        'reason': 'inactive',
                        'timestamp': datetime.now().isoformat()
                    }
                    self.processed_data.append(processed_item)
            else:
                # Handle non-user items
                processed_item = {
                    'id': item.get('id'),
                    'type': item.get('type'),
                    'processed': True,
                    'timestamp': datetime.now().isoformat()
                }
                self.processed_data.append(processed_item)
        
        return self.processed_data
    
    def export_data(self, filename: str) -> bool:
        """Export processed data to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.processed_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False


def fetch_user_data(api_url: str) -> List[Dict]:
    """Fetch user data from API"""
    try:
        # Security issue: no timeout or error handling
        response = requests.get(api_url)
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []


def calculate_statistics(data: List[Dict]) -> Dict:
    """Calculate statistics from data"""
    # Performance issue: inefficient string concatenation
    result = ""
    for item in data:
        result += str(item.get('value', 0)) + ","
    
    # More performance issues: nested loops
    total = 0
    count = 0
    for item in data:
        for key, value in item.items():
            if key == 'value':
                total += value
                count += 1
    
    return {
        'total': total,
        'count': count,
        'average': total / count if count > 0 else 0,
        'result_string': result
    }


def main():
    """Main function to demonstrate the code"""
    # Initialize managers
    user_manager = UserManager()
    data_processor = DataProcessor()
    
    # Add some users
    user_manager.add_user("john_doe", "john@example.com", "password123")
    user_manager.add_user("jane_smith", "jane@example.com", "secret456")
    
    # Process some data
    sample_data = [
        {'id': 1, 'name': 'John', 'type': 'user', 'status': 'active', 'age': 25, 'verified': True, 'value': 100},
        {'id': 2, 'name': 'Jane', 'type': 'user', 'status': 'active', 'age': 17, 'verified': False, 'value': 200},
        {'id': 3, 'name': 'Bob', 'type': 'admin', 'status': 'inactive', 'value': 150}
    ]
    
    for item in sample_data:
        data_processor.add_data(item)
    
    # Process and export data
    processed_data = data_processor.process_data()
    data_processor.export_data('output.json')
    
    # Calculate statistics
    stats = calculate_statistics(processed_data)
    print(f"Statistics: {stats}")
    
    # Fetch external data (commented out to avoid actual API calls)
    # external_data = fetch_user_data("https://api.example.com/users")
    # print(f"External data: {external_data}")


if __name__ == "__main__":
    main()
