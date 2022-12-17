# Google Cloud Compute VM Cleanup

Script to delete oldest VM in a project.  

## Usage

```shell
$ python3 cleanup.py --project_id GOOGLE_CLOUD_PROJECT_ID_NAME \
                     --zone GCP_ZONE \
                     --service_name_label SERVICE_TAG
```

Example:

```shell
$ python3 cleanup.py --project_id my-gcp-project123456789 \
                     --zone us-central1-a \
                     --service_name_label my-service
```

`--project_id` Google Cloud Project ID.  

`--zone` Google Cloud zone in which the VM exists in.  

`--service_name_label` A label on the Compute VM in the format of `service: LABEL`.  
So if the label is `service: database` then use the field `--service_name_label database`.  
Make sure to use the **label** feature on the VM and not the **tag**.  

## Running on GCP

1. Make a Service Account with the capability to read, write, and delete Compute VMs.  
1. When creating the VMs, attach the Service Account you created to the VM.  

## Running on local machine

1. Make a Service Account with the capability to read, write, and delete Compute VMs.  
1. Authenticate on local machine.  
    a. Generate the API keys and run `export GOOGLE_APPLICATION_CREDENTIALS=location of your API KEY file`

## Common pitfalls  

Make sure to use the **label** feature on the VM and not the **tag**.  
