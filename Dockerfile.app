FROM python:3.11

WORKDIR /root

RUN pip install uvicorn fastapi pandas scikit-learn

COPY app/ app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]