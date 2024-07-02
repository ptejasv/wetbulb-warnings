FROM python:3.10.14-slim

WORKDIR /app

COPY src/requirements.txt /app/src/

RUN pip3 install -r src/requirements.txt

COPY . /app/

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

WORKDIR /app/src

CMD ["streamlit", "run", "wetbulb_warnings.py"]
