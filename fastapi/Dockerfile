FROM python:3.10-alpine
# used with live-reload so .pyc isn't stored on host
ENV PYTHONPYCACHEPREFIX=/tmp
#/
RUN pip install virtualenv
RUN virtualenv venv
RUN source venv/bin/activate
WORKDIR /app
EXPOSE 5000
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "/app/src/main.py"]
