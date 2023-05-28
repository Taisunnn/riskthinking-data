FROM python:3.11

ENV AIRFLOW_HOME=/root
ENV AIRFLOW__CORE__LOAD_EXAMPLES=false

WORKDIR /root

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

COPY dags/ dags/
COPY data_in/ data_in/

ENTRYPOINT ["./docker-entrypoint.sh"]