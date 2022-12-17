FROM python:latest
ENV PROJECT_ID=""
ENV ZONE=""
ENV SERVICE_NAME=""
COPY . .
RUN pip install --upgrade pip \
    pip install -r requirements.txt
CMD python3 cleanup.py --gcp_project_id ${PROJECT_ID} \
    --gcp_zone ${ZONE} \
    --service_name_label ${SERVICE_NAME}