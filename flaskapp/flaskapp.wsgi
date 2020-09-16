import sys
sys.path.insert(0, '/var/www/html/flaskapp')
sys.path.append('/home/ubuntu/flaskapp/venv/bin')
sys.path.append('/home/ubuntu/flaskapp/venv/lib/python3.7/site-packages')
sys.path.append('/home/ubuntu/flaskapp/venv/lib/python3.7')

from flaskapp import app as application