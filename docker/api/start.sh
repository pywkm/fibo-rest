#!/bin/sh

gunicorn 'api.app:get_app()' -c ./api/gunicorn.conf.py --reload
