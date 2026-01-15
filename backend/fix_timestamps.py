#!/usr/bin/env python3
"""
Fix timestamp columns in the students table
Run this script on the server to fix existing invalid timestamps
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from src.config.settings import settings

def fix_timestamps():
    """Fix invalid timestamp values in the database"""
    
    engine = create_engine(settings.db_url)
    
    with engine.connect() as conn:
        print("🔧 Checking and fixing timestamp columns...")
        
        # First, check if columns exist
        try:
            result = conn.execute(text("DESCRIBE students"))
            columns = [row[0] for row in result]
            has_created_at = 'created_at' in columns
            has_updated_at = 'updated_at' in columns
            
            print(f"Columns exist: created_at={has_created_at}, updated_at={has_updated_at}")
            
            # Add columns if they don't exist
            if not has_created_at:
                print("Adding created_at column...")
                conn.execute(text(
                    "ALTER TABLE students ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP"
                ))
                conn.commit()
                print("✅ Added created_at column")
            
            if not has_updated_at:
                print("Adding updated_at column...")
                conn.execute(text(
                    "ALTER TABLE students ADD COLUMN updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
                ))
                conn.commit()
                print("✅ Added updated_at column")
            
            # If columns already existed, fix invalid values
            if has_created_at:
                result = conn.execute(text(
                    "SELECT COUNT(*) as count FROM students WHERE created_at = '0000-00-00 00:00:00' OR created_at IS NULL"
                ))
                invalid_created = result.fetchone()[0]
                
                if invalid_created > 0:
                    conn.execute(text(
                        "UPDATE students SET created_at = CURRENT_TIMESTAMP WHERE created_at = '0000-00-00 00:00:00' OR created_at IS NULL"
                    ))
                    conn.commit()
                    print(f"✅ Fixed {invalid_created} invalid created_at timestamps")
            
            if has_updated_at:
                result = conn.execute(text(
                    "SELECT COUNT(*) as count FROM students WHERE updated_at = '0000-00-00 00:00:00' OR updated_at IS NULL"
                ))
                invalid_updated = result.fetchone()[0]
                
                if invalid_updated > 0:
                    conn.execute(text(
                        "UPDATE students SET updated_at = CURRENT_TIMESTAMP WHERE updated_at = '0000-00-00 00:00:00' OR updated_at IS NULL"
                    ))
                    conn.commit()
                    print(f"✅ Fixed {invalid_updated} invalid updated_at timestamps")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return
        
        # Show sample of fixed data
        print("\n📊 Sample of records:")
        result = conn.execute(text(
            "SELECT id, name, index_number, created_at, updated_at FROM students ORDER BY id LIMIT 5"
        ))
        for row in result:
            print(f"  {row.id}: {row.name} - created: {row.created_at}, updated: {row.updated_at}")
        
        print("\n✨ Timestamp fix completed!")

if __name__ == "__main__":
    fix_timestamps()
