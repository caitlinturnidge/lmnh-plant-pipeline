FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY extract.py .
COPY load.py .
COPY rds_to_s3.py .
COPY pipeline.py .

CMD [ "pipeline.handler" ] 