FROM public.ecr.aws/lambda/python:3.10
COPY --from=piplock /Pipfile.lock ${LAMBDA_TASK_ROOT}
COPY . ${LAMBDA_TASK_ROOT}
RUN pip install pipenv
RUN pipenv requirements > requirements.txt
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
CMD [ "lambda_function.lambda_handler" ]`

# BUILD COMMAND
# docker buildx build -t top_stock_raw_data_enrichment_transformer:tag . --build-context piplock=../../../
