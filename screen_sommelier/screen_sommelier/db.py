# import sqlite3
import click
from flask import current_app, g
import psycopg2
from psycopg2.extras import RealDictCursor

# SQLite3 get_db command
# def get_db():
#     if 'db' not in g:
#         g.db = sqlite3.connect(
#             current_app.config['DATABASE'],
#             detect_types=sqlite3.PARSE_DECLTYPES
#         )
#         g.db.row_factory = sqlite3.Row

#     return g.db

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host = current_app.config['DATABASE']['HOST'],
            database = current_app.config['DATABASE']['DB'],
            user = current_app.config['DATABASE']['USER'],
            password = current_app.config['DATABASE']['PASSWORD'],
            port = current_app.config['DATABASE']['PORT']
        )

    if 'curs' not in g:
        g.curs = g.db.cursor(cursor_factory = RealDictCursor)

    return g.db, g.curs

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
