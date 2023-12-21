FROM python:latest

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt \
    && pip install --upgrade cython \
    && pip install pymssql==2.2.11

COPY image_data_STATIC.csv .
COPY origin_data_STATIC.csv .
COPY mock_data_multi_plants.csv .
COPY data_utils.py .
COPY db_functions.py .
COPY main.py .
COPY config.toml

EXPOSE 8501

CMD streamlit run main.py --server.port 8501
