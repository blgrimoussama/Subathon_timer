from app.app import app

if __name__ == "__main__":
  app.secret_key = "my_secret_key"
  app.run('0.0.0.0', 8080, debug=True)

