from app.app import app

if __name__ == "__main__":
  app.secret_key = "my_secret_key"
  app.run(host='0.0.0.0', port=8080, debug=True)

