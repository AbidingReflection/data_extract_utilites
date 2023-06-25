import os
import sqlite3

from datetime import datetime, timedelta

from config import CONFIG
from initialize import validate_targets, get_db_list, handle_args
from db_utils import get_databases

def get_archive_path() -> str:
    '''Returns path of archive db in search_dir. \n
       Creates archive SQLite db if one does not exist'''
    
    def create_archive(path_str: str):
        '''Creates new archive SQLite db'''

        con = sqlite3.connect(path_str)
        cur = con.cursor()
        
        query = '''CREATE TABLE "extract_metric_archive" (
                                "extract_ts" TEXT,
                                "artifact_type"	TEXT,
                                "start_time"	INTEGER,
                                "end_time"	INTEGER,
                                "seconds_elapsed"	INTEGER,
                                "api_call_count"	INTEGER,
                    PRIMARY KEY("extract_ts", "artifact_type"))'''
                    
        cur.execute(query)
        con.commit()
        
    file_name = CONFIG["archive_name"]
    path_str = args.search_dir + "/" + file_name
    
    # Check for existing archive in target dir
    if not(os.path.exists(path_str) and os.path.isfile(path_str)):
        create_archive(path_str)
        
    return path_str

    
args = handle_args()
validate_targets(args)

db_names = get_db_list(args)
# print(db_names)
databases = get_databases(args, db_names)

archive_path = get_archive_path()
filter_datetime = datetime.now() - timedelta(days=CONFIG["archive_day_threshold"])

db_list = [databases[db_str] for db_str in databases if databases[db_str].extract_time < filter_datetime]


# filter dbs outside of day range
# Process load metrics to archive
# Move to recycling bin like folder
# Update extract to process existing archives