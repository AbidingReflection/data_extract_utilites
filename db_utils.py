import argparse
from dataclasses import dataclass
import datetime
import sqlite3


@dataclass
class Record:
    '''A class to represent a record.'''
    
    api_call_count: int
    artifact_type: str
    seconds_elapsed:int


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

        path_str = args.search_dir + '/' + self.file_name
        
        con = sqlite3.connect(path_str)
        cur = con.cursor()
        
        cur.execute(''' SELECT  artifact_type,
                                seconds_elapsed,
                                api_call_count
                        FROM extract_metrics''')
        data = cur.fetchall()
        
        records = []
        for row in data:
            record = Record(artifact_type=row[0],
                            seconds_elapsed=row[1],
                            api_call_count=row[2])
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
            record_entry = {"timestamp": str(databases[db].extract_time),
                            "api_call_count":record.api_call_count,
                            "artifact_type":record.artifact_type,
                            "seconds_elapsed":record.seconds_elapsed}
            
            records.append(record_entry)
    return records