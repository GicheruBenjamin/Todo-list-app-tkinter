# app/main.py

# == Entry point ==
from app.config import provide_app_settings, provide_theme_settings, load_db_settings
from app.db import init_sqlite, close_sqlite
from app.utils import build_query


def main():
    app_settings = provide_app_settings()
    theme_settings = provide_theme_settings()
    db_settings = load_db_settings()

    print(app_settings)
    print(theme_settings)
    print(db_settings)

    connection = init_sqlite(db_settings)
    print(connection)
    close_sqlite(connection)

    sample_query = {
         "filters": {
             "logic": "AND",
             "conditions": [
                 {
                     "field": "status",
                     "operator": "eq",
                     "value": "done",
                 },
                 {
                     "field": "priority",
                     "operator": "eq",
                     "value": "high",
                 },
             ],
         },
         "sorts": [
             {
                 "field": "title",
                 "order": "asc",     #asc or desc
             },
         ],
         "page_set": {
             "page_no": 1,
             "page_limit": 10,
             "offset": 0,
             "start": None,
             "finish": None,
         },
         "projection": {
             "include": ["title", "status", "priority", "created_at"],
             "exclude": None,
         },
    }

    sql, params = build_query("tasks", sample_query)
    print(sql)
    print(params)




if __name__ == "__main__":
    main()