"""Delete the oldest VM in Google Cloud project."""

import datetime

from absl import app
from absl import flags
from absl import logging

from google.api_core.extended_operation import ExtendedOperation
from google.cloud import compute_v1

flags = flags.FLAGS
flags.DEFINE_string("project_id", "", "Google Cloud Project ID.")
flags.DEFINE_string("zone", "", "Google Cloud Zone. us-central1-c, etc.")
flags.DEFINE_string("service_name_label", "",
                    "Label on VM to be considered for deletion.")

PROJECT_ID = flags.project_id
ZONE = flags.zone
SERVICE_NAME_LABEL = flags.service_name_label


def main(_):
    client: compute_v1.InstancesClient = compute_v1.InstancesClient()
    oldest_vm: tuple[str, datetime.datetime |
                     None] = get_oldest_vm(client, SERVICE_NAME_LABEL)
    if oldest_vm[1] is None:
        logging.info("There is no older VM for this service.")
        exit()
    else:
        logging.info("Attempting to terminate oldest VM.")
        operation = client.delete(
            project=PROJECT_ID, zone=ZONE, instance=oldest_vm[0])
        wait_for_extended_operation(operation, "Delete instance")
        logging.info("Deleting oldest VM %s in zone %s started at %s success.",
                     oldest_vm[0], ZONE, oldest_vm[1])


def get_oldest_vm(client: compute_v1.InstancesClient,
                  service_name_label: str) -> tuple[str, datetime.datetime | None]:
    """Return list of non-terminated Compute VMs."""

    oldest_candidate: tuple[str, datetime.datetime] = ("", None)

    for instance in client.list(project=PROJECT_ID, zone=ZONE):
        logging.info("Looking at VM: %s %s", instance.name, instance.status)

        if instance.labels["service"] == service_name_label and instance.status == "RUNNING":
            print(oldest_candidate)
            if oldest_candidate[1] is None:
                oldest_candidate = (instance.name, datetime.datetime.fromisoformat(
                    instance.creation_timestamp))
            else:
                instance_timestamp: datetime.datetime = datetime.datetime.fromisoformat(
                    instance.creation_timestamp)
                if oldest_candidate[1] > instance_timestamp:
                    oldest_candidate = (instance.name, instance_timestamp)

    logging.info(
        "Oldest VM for %s service is %s created at %s", service_name_label,
        oldest_candidate[0], oldest_candidate[1])
    return oldest_candidate


def wait_for_extended_operation(
    operation: ExtendedOperation, verbose_name: str = "operation", timeout: int = 300


) -> any:
    """
    This method will wait for the extended (long-running) operation to
    complete. If the operation is successful, it will return its result.
    If the operation ends with an error, an exception will be raised.
    If there were any warnings during the execution of the operation
    they will be printed to logging.

    Args:
        operation: a long-running operation you want to wait on.
        verbose_name: (optional) a more verbose name of the operation,
            used only during error and warning reporting.
        timeout: how long (in seconds) to wait for operation to finish.
            If None, wait indefinitely.

    Returns:
        Whatever the operation.result() returns.

    Raises:
        This method will raise the exception received from `operation.exception()`
        or RuntimeError if there is no exception set, but there is an `error_code`
        set for the `operation`.

        In case of an operation taking longer than `timeout` seconds to complete,
        a `concurrent.futures.TimeoutError` will be raised.
    """
    result = operation.result(timeout=timeout)

    if operation.error_code:
        logging.error(
            "Error during %s: [Code: %s]: %s",
            verbose_name, operation.error_code, operation.error_message)
        raise operation.exception() or RuntimeError(operation.error_message)

    if operation.warnings:
        logging.warning("Warnings during %s:\n", verbose_name)
        for warning in operation.warnings:
            logging.warning(" - %s: %s",
                            warning.code, warning.message)

    return result


if __name__ == "__main__":
    app.run(main)
