FROM python:3.11-alpine
RUN apk add build-base linux-headers
COPY . /application
WORKDIR /application
RUN apk add g++
RUN pip install gevent
RUN pip install -r requirements.txt
# CMD ["python", "main.py"]
# CMD ["python", "test_socket.py", "&", "gunicorn", "-b", "0.0.0.0:8000", "main:app", "--worker-class", "gevent"]
# CMD ["gunicorn -b 0.0.0.0:8000 main:app --worker-class gevent;python test_socket.py"]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "main:app", "--worker-class", "gevent"]
