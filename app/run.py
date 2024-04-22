# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from pprint import pprint

import os
from   flask_migrate import Migrate
from   flask_minify  import Minify
from   sys import exit

from api_generator.commands import gen_api

# Debugging extensions that allow for live debugging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from apps.config import config_dict
from apps import create_app, db

# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')
    
def on_reload():
    observer = Observer()

    # Watch for changes in the static directory
    observer.schedule(
        FileSystemEventHandler(), 
        path='static/', 
        recursive=True
    )

    # Watch for changes in the templates directory
    observer.schedule(
        FileSystemEventHandler(), 
        path='templates/', 
        recursive=True
    )

    observer.start()

app = create_app(app_config)
Migrate(app, db)

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)

for command in [gen_api, ]:
    app.cli.add_command(command)
    
if __name__ == '__main__':
    
    with app.app_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                print(rule.endpoint)
                
    app.run()
