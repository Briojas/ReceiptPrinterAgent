#!/usr/bin/env python3
"""AI Agent for iOS Reminders task extraction."""

import asyncio
import datetime
import os
import json
from typing import List, Optional, Dict, Any

from dotenv import load_dotenv
from pydantic import BaseModel

from src.database.task_db import TaskDatabase, TaskRecord

# Load environment variables
load_dotenv()


class Task(BaseModel):
    """Task model for extracted iOS Reminders tasks."""

    name: str
    priority: int  # 1 for high, 2 for medium, 3 for low
    due_date: Optional[str] = None  # ISO format date string
    completed: bool = False
    list_name: Optional[str] = None  # The iOS Reminders list name


class ImportantTasks(BaseModel):
    """Container for extracted tasks and summary."""

    tasks: List[Task]
    summary: str


class IosRemindersExtractor:
    """Handles extraction of tasks from iOS Reminders."""
    
    def __init__(self, credentials_file: Optional[str] = None):
        """
        Initialize the iOS Reminders extractor.
        
        Args:
            credentials_file: Optional path to a file containing iCloud credentials
        """
        self.credentials_file = credentials_file or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            "credentials", 
            "icloud_credentials.json"
        )
    
    def _get_credentials(self) -> Dict[str, str]:
        """
        Get iCloud credentials from file or environment variables.
        
        Returns:
            Dictionary containing 'username' and 'password'
        """
        # Try environment variables first
        username = os.getenv("ICLOUD_USERNAME")
        password = os.getenv("ICLOUD_PASSWORD")
        
        if username and password:
            return {"username": username, "password": password}
        
        # Try credentials file if it exists
        if os.path.exists(self.credentials_file):
            try:
                with open(self.credentials_file, 'r') as f:
                    creds = json.load(f)
                    if 'username' in creds and 'password' in creds:
                        return creds
            except Exception as e:
                print(f"Error reading credentials file: {e}")
        
        # If nothing found, prompt the user
        print("\niCloud credentials not found in environment or credentials file.")
        username = input("Enter your iCloud email: ")
        password = input("Enter your iCloud password: ")
        
        # Save for future use if desired
        save = input("Save these credentials for future use? (y/n): ").lower() == 'y'
        if save:
            os.makedirs(os.path.dirname(self.credentials_file), exist_ok=True)
            with open(self.credentials_file, 'w') as f:
                json.dump({"username": username, "password": password}, f)
        
        return {"username": username, "password": password}
    
    async def extract_tasks(self) -> ImportantTasks:
        """
        Extract tasks from iOS Reminders.
        
        Returns:
            ImportantTasks object containing extracted tasks and summary
        """
        try:
            # Get credentials
            credentials = self._get_credentials()
            
            # Extract tasks using pyicloud (will be implemented)
            tasks = await self._extract_tasks_from_icloud(
                credentials["username"], 
                credentials["password"]
            )
            
            # Create summary
            due_soon = sum(1 for task in tasks if task.due_date and task.due_date <= datetime.datetime.now().isoformat())
            high_priority = sum(1 for task in tasks if task.priority == 1)
            
            summary = (
                f"Found {len(tasks)} tasks in iOS Reminders. "
                f"{due_soon} tasks are due soon. "
                f"{high_priority} tasks are high priority."
            )
            
            return ImportantTasks(tasks=tasks, summary=summary)
        
        except Exception as e:
            print(f"Error extracting tasks: {e}")
            # Return empty result on error
            return ImportantTasks(tasks=[], summary=f"Error: {str(e)}")
    
    async def _extract_tasks_from_icloud(self, username: str, password: str) -> List[Task]:
        """
        Extract tasks from iCloud Reminders.
        
        Args:
            username: iCloud email
            password: iCloud password
            
        Returns:
            List of Task objects
        """
        try:
            # This is a placeholder for the actual implementation
            # In a real implementation, we would use pyicloud:
            # from pyicloud import PyiCloudService
            # api = PyiCloudService(username, password)
            # Handle 2FA if needed
            # Extract reminders from api.reminders
            
            # For now, we'll return placeholder tasks for demonstration
            print("Note: This is a placeholder implementation. Real iCloud integration will need to be implemented.")
            
            # Placeholder tasks
            tasks = [
                Task(
                    name="Sample iOS Reminder 1",
                    priority=1,
                    due_date=datetime.datetime.now().isoformat(),
                    list_name="Work"
                ),
                Task(
                    name="Sample iOS Reminder 2",
                    priority=2,
                    due_date=(datetime.datetime.now() + datetime.timedelta(days=1)).isoformat(),
                    list_name="Personal"
                )
            ]
            
            return tasks
            
        except Exception as e:
            print(f"Error connecting to iCloud: {e}")
            return []


async def extract_ios_reminders_tasks() -> ImportantTasks:
    """
    Public function to extract tasks from iOS Reminders.
    
    Returns:
        ImportantTasks object containing extracted tasks and summary
    """
    extractor = IosRemindersExtractor()
    return await extractor.extract_tasks()


async def main():
    """Main entry point for the iOS Reminders task extraction agent."""
    print("=" * 50)
    print("iOS REMINDERS TASK EXTRACTION AGENT")
    print("=" * 50)

    # Initialize database
    db = TaskDatabase()

    try:
        print("\n📱 Connecting to iOS Reminders...")
        print("🔄 Processing...")

        # Extract tasks
        result = await extract_ios_reminders_tasks()

        if result and result.tasks:
            print(f"\n✅ Found {len(result.tasks)} tasks")
            print("\n📊 SUMMARY:")
            print(f"   {result.summary}")

            print("\n📋 EXTRACTED TASKS:")
            priority_map = {1: "🔴 HIGH", 2: "🟡 MEDIUM", 3: "🟢 LOW"}

            # Process and store tasks
            new_tasks = []
            duplicate_tasks = []

            for i, task in enumerate(result.tasks, 1):
                print(f"\n{i}. {task.name}")
                print(f"   Priority: {priority_map.get(task.priority, '❓ UNKNOWN')}")
                if task.due_date:
                    print(f"   Due: {task.due_date}")
                if task.list_name:
                    print(f"   List: {task.list_name}")

                # Check for duplicates
                is_duplicate = False
                similar_tasks = db.find_similar_tasks(task.name)
                if (
                    similar_tasks
                    and len(similar_tasks) > 0
                    and similar_tasks[0].similarity_distance < 0.1
                ):
                    is_duplicate = True
                    duplicate_tasks.append(task)
                    continue

                # Add new task to database
                db_task = TaskRecord(
                    name=task.name,
                    priority=task.priority,
                    due_date=task.due_date or datetime.datetime.now().isoformat(),
                    created_at=datetime.datetime.now().isoformat(),
                )
                db.add_task(db_task)
                new_tasks.append(task)

            # Print summary of database operations
            if new_tasks:
                print(f"\n💾 Saved {len(new_tasks)} new tasks to database")
            if duplicate_tasks:
                print(
                    f"\n🔁 Found {len(duplicate_tasks)} duplicate tasks that were not saved:"
                )
                for task in duplicate_tasks:
                    print(f"   - {task.name}")

            # Prompt to print tasks
            print_tasks = input("\nDo you want to print these tasks to receipt printer? (y/n): ")
            if print_tasks.lower() == 'y':
                print("\n🖨️ Sending tasks to printer...")
                # Import here to avoid circular imports
                from src.task_card_generator import create_task_image, print_to_thermal_printer
                
                for task in new_tasks:
                    task_data = {
                        "title": task.name,
                        "priority": priority_map.get(task.priority, "UNKNOWN"),
                        "due_date": task.due_date or "Today",
                        "list": task.list_name or "Default"
                    }
                    
                    # Create and print task image
                    image_path = create_task_image(task_data)
                    if image_path:
                        try:
                            print(f"   Printing: {task.name}")
                            print_to_thermal_printer(image_path)
                        except Exception as e:
                            print(f"   ⚠️ Printing failed: {e}")
                
                print("   ✅ Printing complete!")
                    
        else:
            print("\n❌ No actionable tasks found in iOS Reminders")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

    print("\n" + "=" * 50)
    # Close database connection
    db.close()


if __name__ == "__main__":
    asyncio.run(main())
