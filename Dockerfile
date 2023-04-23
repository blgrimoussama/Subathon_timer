FROM python:3.11-alpine
COPY . /application
WORKDIR /application
RUN apk --no-cache add musl-dev linux-headers g++
RUN pip install numpy
RUN pip install -r requirements.txt
# RUN pip install requests Flask Flask-Cors Flask-OAuthlib Flask-WTF pymongo python-dotenv
CMD ["python", "app.py"]

