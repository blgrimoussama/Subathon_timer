# from app.app import app
# import logging 
# logging.basicConfig(level='DEBUG')

# logging.info('hello world')

# app = app

# logging.info(f'App: {app}')

# if __name__ == "__main__":
#   app.secret_key = "my_secret_key"
#   app.run(host='0.0.0.0', port=8080, debug=True)

from app.app import app
from app.credentials import APP_SECRET_KEY

if __name__ == "__main__":
  app.secret_key = APP_SECRET_KEY
  app.run(host='0.0.0.0', port=8080, debug=True)
