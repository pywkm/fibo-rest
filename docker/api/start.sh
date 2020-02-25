#!/bin/sh

gunicorn api.app:app -c ./api/gunicorn.conf.py --reload
