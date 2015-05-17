bind = 'unix:/tmp/gunicorn.sock'
backlog = 2048
workers = 4
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 120