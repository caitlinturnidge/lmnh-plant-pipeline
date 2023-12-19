FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY s3_data_management.py .

CMD [ "s3_data_management.handler" ] 