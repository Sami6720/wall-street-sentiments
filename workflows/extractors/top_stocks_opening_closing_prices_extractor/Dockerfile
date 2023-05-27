FROM public.ecr.aws/lambda/python:3.10
COPY . ${LAMBDA_TASK_ROOT}
RUN pip install requests --target "${LAMBDA_TASK_ROOT}"
RUN pip install pandas --target "${LAMBDA_TASK_ROOT}"
RUN pip install boto3 --target "${LAMBDA_TASK_ROOT}"
RUN pip install beautifulsoup4 --target "${LAMBDA_TASK_ROOT}"
RUN pip install pyyaml --target "${LAMBDA_TASK_ROOT}"
RUN pip install ipykernel --target "${LAMBDA_TASK_ROOT}"
RUN pip install pytz --target "${LAMBDA_TASK_ROOT}"
CMD [ "lambda_function.lambda_handler" ]`