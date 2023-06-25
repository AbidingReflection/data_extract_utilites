import argparse
from dataclasses import dataclass
import datetime
import sqlite3
from config import CONFIG


@dataclass
class Record:
    '''A class to represent a record.'''        
    artifact_type: str
    seconds_elapsed: int
    api_call_count: int


@dataclass
class Database:
    '''A class to represent a database.
    
    Methods:
    -------
    get_records(self, args:argparse.Namespace)
    
    '''
    
    file_name: str
    extract_time: datetime
    records: list[Record]
    
    def get_records(self, args:argparse.Namespace) -> list[Record]:
        '''Returns all db records from Database in a list'''
        
        def get_query_str():
            col_str = ""
            for col in CONFIG["extract_cols"]:
                col_str = col_str + col + ", "
            if len(col_str) > 2:
                col_str = col_str[:-2]
            
            query_str = f'''SELECT {col_str}
                        FROM {CONFIG["db_table_target"]}
                         '''

            return query_str

        path_str = args.search_dir + '/' + self.file_name
        
        con = sqlite3.connect(path_str)
        cur = con.cursor()
        
        query_str = get_query_str()

        cur.execute(query_str)
        data = cur.fetchall()
        
        records = []
        
        for row in data:
            record = Record(*row)
            records.append(record)
        
        return records
    
       
def db_name_to_datetime(db_name: str) -> datetime:
    '''Returns datetime object from database name formated as timestamp.'''
    
    year = db_name[0:4]
    month = db_name[4:6]
    day = db_name[6:8]
    hour = db_name[9:11]
    min = db_name[11:13]
    sec = db_name[13:15]

    extract_time = datetime.datetime(year=int(year),
                                     month=int(month),
                                     day=int(day),
                                     hour=int(hour),
                                     minute=int(min),
                                     second=int(sec))
    
    return extract_time


def get_datetime_str(datetime:datetime) -> str:
    '''Returns db name string from datetime object.'''
    
    return datetime.strftime('%Y%m%d-%H%M%S')
      
      
def get_databases(args: argparse.Namespace, db_names: list[str]) -> dict[Database]:
    '''Returns dict of all Databases in target directory.'''
    
    databases = {}
    for db_name in db_names:
        extract_datetime = db_name_to_datetime(db_name)
        database = Database(file_name=db_name,
                            extract_time=extract_datetime,
                            records=[])
        records = database.get_records(args=args)
        database.records = records
        databases[db_name] = database
        
    return databases
    
    
def extract_records(databases: dict[Database]) -> list[dict]:
    '''Returns list of all records from dict of Databases.'''
    
    records = []
    for db in databases:
        db_records = databases[db].records
        
        for record in db_records:
            record_entry = {"timestamp": str(databases[db].extract_time)}
            
            for col in CONFIG["extract_cols"]:
                record_entry[col] = getattr(record, col)
            
            records.append(record_entry)
    return records