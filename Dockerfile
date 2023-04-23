FROM python:3.11-alpine
RUN apk add build-base linux-headers
COPY . /application
WORKDIR /application
RUN apk add g++ 
RUN pip install numpy
RUN pip install -r requirements.txt
# RUN pip install requests Flask Flask-Cors Flask-OAuthlib Flask-WTF pymongo python-dotenv
CMD ["python", "app.py"]

