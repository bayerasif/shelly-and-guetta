FROM python:3-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 7080
CMD ["python", "shelly-and-guetta.py"]
