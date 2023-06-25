import datetime
import json

from config import CONFIG
from initialize import validate_targets, get_db_list, handle_args
from db_utils import get_databases, extract_records, get_datetime_str

args = handle_args()
validate_targets(args)

db_names = get_db_list(args)
databases = get_databases(args, db_names)
records = extract_records(databases)

# Serialize json
json_object = json.dumps(records, indent=4)

# Build file path
extract_time = get_datetime_str(datetime.datetime.now())
export_file_name = f"{CONFIG['title_prefix']}{extract_time}.json"
export_path = args.export_dir + '/' + export_file_name

# Writing json
with open(export_path, "w") as outfile:
    outfile.write(json_object)

# User Feedback
db_count = len(databases)
record_count = len(records)
print(f'{record_count} records extracted from {db_count} databases')