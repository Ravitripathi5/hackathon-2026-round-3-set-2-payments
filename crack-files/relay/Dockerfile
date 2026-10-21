FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3
COPY relay.py /opt/relay.py
RUN chmod 777 /opt/relay.py
CMD ["python3", "/opt/relay.py"]
