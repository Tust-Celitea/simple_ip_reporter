#!/usr/bin/python
import app
from flask_script import Manager as utils
from flask_migrate import Migrate,MigrateCommand

migrate=Migrate(app.app,app.db)
manager=utils(app.app)
manager.add_command('db',MigrateCommand)

@manager.command
def debug():
    '''Run Debug Server'''
    app.app.run(debug=True)

if __name__=="__main__":
    manager.run()
