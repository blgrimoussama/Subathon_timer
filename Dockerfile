FROM python:3.11-alpine
RUN apk add build-base linux-headers
COPY . /application
WORKDIR /application
RUN apk add g++ 
RUN pip install -r requirements.txt
CMD ["python", "main.py"]