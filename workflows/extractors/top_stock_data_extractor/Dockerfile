FROM public.ecr.aws/lambda/python:3.10
COPY --from=piplock /Pipfile.lock ${LAMBDA_TASK_ROOT}
COPY . ${LAMBDA_TASK_ROOT}
ARG FINHUB_API_KEY
ENV FINHUB_API_KEY=$FINHUB_API_KEY
ARG BUCKET_NAME
ENV BUCKET_NAME=$BUCKET_NAME
RUN pip install pipenv
RUN pipenv requirements > requirements.txt
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
CMD [ "lambda_function.lambda_handler" ]`
