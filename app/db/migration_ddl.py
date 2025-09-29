# app/db/migration_ddl.py

# Migration_ddl for the tables and their columns
# In the db..
# app/db/migration_ddl.py

# == Tables ==
create_task_table = """
CREATE TABLE IF NOT EXISTS task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL,
    task_name TEXT NOT NULL,
    task_description TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'completed', 'archived', 'deleted')),
    priority TEXT NOT NULL CHECK (priority IN ('low', 'medium', 'high')),
    occurrence TEXT NOT NULL CHECK (occurrence IN ('daily', 'weekly', 'monthly')),
    due_date TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    category_id TEXT
);
"""

create_category_table = """
CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id TEXT NOT NULL,
    category_name TEXT NOT NULL,
    category_color TEXT NOT NULL CHECK (category_color IN (
        'red_purple', 'blue_violet', 'green_yellow', 'yellow_green', 'orange', 'pink'
    )),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

# == Indexes ==
create_indexes = """
CREATE INDEX IF NOT EXISTS task_task_id_index ON task (task_id);
CREATE INDEX IF NOT EXISTS category_category_id_index ON category (category_id);
"""

# == Triggers ==
create_task_updated_at_trigger = """
CREATE TRIGGER IF NOT EXISTS task_updated_at_trigger
AFTER UPDATE ON task
FOR EACH ROW
BEGIN
    UPDATE task
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;
"""

create_category_updated_at_trigger = """
CREATE TRIGGER IF NOT EXISTS category_updated_at_trigger
AFTER UPDATE ON category
FOR EACH ROW
BEGIN
    UPDATE category
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;
"""

# == Migration order ==
MIGRATION_DDL = [
    create_task_table,
    create_category_table,
    create_indexes,
    create_task_updated_at_trigger,
    create_category_updated_at_trigger,
]