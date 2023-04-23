FROM python:3.11-alpine
ADD repositories /etc/apk/repositories
apk --no-cache add musl-dev linux-headers g++
COPY . /application
WORKDIR /application
RUN pip install -r requirements.txt
# RUN pip install requests Flask Flask-Cors Flask-OAuthlib Flask-WTF pymongo python-dotenv
CMD ["python", "app.py"]

