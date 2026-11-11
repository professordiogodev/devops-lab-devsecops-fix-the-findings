FROM python:latest
ADD https://example.com/tools/healthprobe.tgz /tmp/
RUN apt-get update && apt-get install -y curl vim
COPY service /app
RUN pip install -r /app/requirements.txt
EXPOSE 8000
CMD ["python", "/app/main.py"]
