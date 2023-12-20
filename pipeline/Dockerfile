FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}


RUN pip install --upgrade cython
RUN pip install pymssql

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY extract.py .
COPY load.py .
COPY rds_to_s3.py .
COPY pipeline.py .

CMD [ "pipeline.handler" ] 