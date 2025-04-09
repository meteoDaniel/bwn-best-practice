FROM python:3.12.8-slim

COPY ./requirements.txt /opt/requirements.txt
RUN pip --no-cache-dir install -r /opt/requirements.txt

WORKDIR /app

ENV PYTHONPATH="/app:/app"

COPY . .

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["src.run.handler"]
