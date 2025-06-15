bind = "0.0.0.0:8000"
workers = 2
worker_class = "eventlet" 
worker_connections = 1000
keepalive = 5
errorlog = "-"
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'