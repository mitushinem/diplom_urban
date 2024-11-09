FROM python:latest
WORKDIR /APP
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
