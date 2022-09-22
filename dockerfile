FROM python:latest
WORKDIR /app
COPY  app/requirements.txt .
RUN pip install -r requirements.txt
COPY app/app.py .
EXPOSE 5000
CMD ["flask","run", "--host=0.0.0.0"]