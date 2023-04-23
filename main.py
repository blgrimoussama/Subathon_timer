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

app = app


if __name__ == "__main__":
  app.secret_key = "my_secret_key_Br41N_F@c3"
  app.run(host='0.0.0.0', port=8080, debug=True)