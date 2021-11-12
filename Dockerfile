FROM python:3.8.5-slim
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "shelly-and-guetta.py"]
