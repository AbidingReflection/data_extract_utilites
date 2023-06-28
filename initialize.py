import argparse
import os
import re
import sys

from config import CONFIG

def handle_args() -> argparse.Namespace:
    '''Sets up runtime arguments for search_dir & export_dir.'''
    
    description=''
    parser = argparse.ArgumentParser(description)
    parser.add_argument('search_dir')
    parser.add_argument('export_dir')
    args_ns = parser.parse_args()
    return args_ns


def validate_targets(args:argparse.Namespace):
    '''Validates the target & destination path args.'''
    
    # check targets exists and are folders
    def is_valid_target(path):
        return os.path.exists(path) and os.path.isdir(path)
    
    # Search directory path validation
    if not is_valid_target(args.search_dir):
        sys.exit(f'Search directory invalid: "{args.search_dir}"') 
        
    # Export directory path validation
    if not is_valid_target(args.export_dir):
        sys.exit(f'Export directory invalid: "{args.export_dir}"')


def get_db_list(args:argparse.Namespace)  -> list[str]:
    '''Returns list of Databases name strings in search_dir.'''
    
    # Check for existing files in target dir
    files = os.listdir(args.search_dir)

    # Check for existing .db files in target dir
    db_files = [file for file in files if file[-3:] == ".db"]
    if not db_files:
        sys.exit(f'No .db files found: "{args.export_dir}"')
    
    # Check for formated .db files in target dir
    fmt_db_files = [db_file for db_file in db_files if re.search(CONFIG["db_file_regex_filter"], db_file)]
    if not fmt_db_files:
        sys.exit(f'No properly formated .db files found: "{args.export_dir}"')
    return fmt_db_files
