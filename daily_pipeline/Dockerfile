FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

RUN pip install --upgrade cython
RUN pip install pymssql

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY update_duties.py .
COPY database_functions.py .
COPY s3_data_management.py .
COPY daily_pipeline.py .

CMD [ "daily_pipeline.handler" ] 