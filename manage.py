#!/usr/bin/env python
"""
🚀 DJANGO MANAGEMENT SCRIPT
This is the main command center for your Django project!
"""

import os
import sys

def main():
    """
    🎯 MAIN FUNCTION - Sets up Django and runs commands
    """
    # 📍 Tell Django where to find settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        # 📍 Import Django's command executor
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # ❌ If Django is not installed properly
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # 🎯 Execute the command (like runserver, migrate, etc.)
    execute_from_command_line(sys.argv)

# 📍 This makes the script runnable
if __name__ == '__main__':
    main()