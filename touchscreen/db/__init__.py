
import sys, os
from peewee import SqliteDatabase
from peewee import Model
from peewee import CharField

dbfile = os.path.join(
    os.path.dirname(__file__), 'touchscreen.db'
)

DB = SqliteDatabase(dbfile)


class ApplicationState(Model):
    mode = CharField()

    class Meta:
        database = DB


def start_up():
    DB.connect()
    DB.create_tables([ApplicationState])
    ApplicationState.delete().execute()

    # here's a hacky import from ../../util/config
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from util.config import config

    print('Reset application state')

    ApplicationState.create(id=1, mode=config['MODE'])
    DB.close()


def get_application_mode():
    return ApplicationState.get(id=1).mode


def set_application_mode(mode):
    if not mode:
        raise ValueError("set_application_mode: mode is null")
    app_state = ApplicationState.get(id=1)
    app_state.mode = mode
    return app_state.save()

