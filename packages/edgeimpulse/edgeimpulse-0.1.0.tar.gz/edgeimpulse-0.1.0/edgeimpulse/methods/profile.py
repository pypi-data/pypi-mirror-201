import logging
from pathlib import Path
from typing import Union, Optional, Any
from pprint import pformat
import tempfile

import edgeimpulse
from edgeimpulse.exceptions import InvalidDeviceException

from edgeimpulse.util import (
    configure_generic_client,
    poll,
    default_project_id_for,
    get_profile_devices,
    upload_pretrained_model_and_data,
)
from edgeimpulse_api import (
    JobsApi,
    LearnApi,
    GetPretrainedModelResponse,
)


class ProfileResponse(GetPretrainedModelResponse):
    def summary(self) -> None:
        """Returns a summary of the profiling results"""
        output = []
        if self.specific_device_selected and self.model and self.model.profile_info:
            if self.model.profile_info.float32:
                output.append("Target results for float32:")
                output.append("===========================")
                output.append(
                    pformat(
                        self.model.profile_info.float32.to_dict(),
                        indent=4,
                        sort_dicts=False,
                    )
                )
                output.append("\n")
            if self.model.profile_info.int8:
                output.append("Target results for int8:")
                output.append("========================")
                output.append(
                    pformat(
                        self.model.profile_info.int8.to_dict(),
                        indent=4,
                        sort_dicts=False,
                    )
                )
                output.append("\n")
        if self.model and self.model.profile_info:
            output.append("Performance on device types:")
            output.append("============================")
            output.append(
                pformat(
                    self.model.profile_info.table.to_dict(), indent=4, sort_dicts=False
                )
            )

        print("\n".join(output))

    @classmethod
    def from_dict(cls, obj: dict):
        """Create an instance of ProfileResponse from a dict"""
        return cls(**obj)


def profile(
    model: Union[Path, str, bytes, Any],
    device: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ProfileResponse:
    """Profiles a tflite model and gives information on memory and time per inference

    Args:
        model (Union[Path, str, bytes, Any]): Path or str (denoting filename), binary model as bytes or in momeoy keras model object.
        device (Optional[str], optional): Target device name as string. Defaults to None
        api_key (Optional[str], optional): The API key for an Edge Impulse project. This can also be set via the module-level variable `edgeimpulse.API_KEY`.

    Raises:
        Exception is unable to start request or get result. TOOD(mat) fill out
        InvalidDeviceException when inputted device is not supported

    Returns:
        ProfileResponse: Structure containing profile information

    """

    # create api and jobs clients
    client = configure_generic_client(
        key=api_key if api_key else edgeimpulse.API_KEY,
        host=edgeimpulse.API_ENDPOINT,
    )
    jobs = JobsApi(client)
    learn = LearnApi(client)

    # derive default project id for client
    project_id = default_project_id_for(client)

    if device:
        profile_devices = get_profile_devices(client)
        if device not in profile_devices:
            raise InvalidDeviceException(device, profile_devices)

    # The API bindings currently require files to be on disk.
    # We will write files to this temporary dir if necessary.
    with tempfile.TemporaryDirectory() as tempdir:
        upload_pretrained_model_and_data(
            tempdir=tempdir,
            client=client,
            project_id=project_id,
            model=model,
            device=device,
            representative_data=None,
        )

    try:
        profile_job = learn.profile_pretrained_model(project_id)
        job_id = profile_job.id
    except Exception as e:
        logging.debug(f"exception starting job for profile after upload [{str(e)}]")
        raise e
    _ = poll(
        jobs_client=jobs,
        project_id=project_id,
        job_id=job_id,
    )
    get_pretrained_model_response = learn.get_pretrained_model_info(project_id)
    profile_response = ProfileResponse.from_dict(
        get_pretrained_model_response.to_dict()
    )
    logging.info(f"{profile_response = }")
    logging.debug(f"{profile_response = !r}")
    return profile_response
