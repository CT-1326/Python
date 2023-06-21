#!/bin/bash
gunicorn index:flask_app -c ./gunicorn_config.py