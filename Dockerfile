FROM python:latest
ENV PROJECT_ID=""
ENV ZONE=""
ENV SERVICE_NAME=""
COPY . .
RUN pip install --upgrade pip \
    pip install -r requirements.txt
CMD python3 cleanup.py --project_id ${PROJECT_ID} \
    --zone ${ZONE} \
    --service_name_label ${SERVICE_NAME}