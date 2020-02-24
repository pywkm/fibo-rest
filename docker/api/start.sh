#!/bin/sh

gunicorn app:app -c gunicorn.conf.py --reload
