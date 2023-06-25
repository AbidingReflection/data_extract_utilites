from config import CONFIG
from initialize import validate_targets, get_db_list, handle_args
from db_utils import get_databases

args = handle_args()
validate_targets(args)

db_names = get_db_list(args)
databases = get_databases(args, db_names)

NotImplemented