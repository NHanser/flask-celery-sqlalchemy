#!/bin/sh
gunicorn -w 4 -b 0.0.0.0:5001 "app:create_app()"