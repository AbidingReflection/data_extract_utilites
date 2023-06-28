CONFIG = {
    "title_prefix": "extract_metrics_",
    "db_table_target": "extract_metrics",
    "extract_cols": ["artifact_type",
                     "seconds_elapsed",
                      "api_call_count"],
    "archive_name": "extract_archive.db",
    "archive_day_threshold": 7,
    "db_file_regex_filter": "^[0-9]{8}-[0-9]{6}"
}