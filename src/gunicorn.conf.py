import multiprocessing

bind = '0.0.0.0:8000'
workers = multiprocessing.cpu_count() // 2
timeout = 30
worker_connections = 1000
