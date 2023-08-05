import logging, re, os, tempfile, shutil
from pathlib import Path
from pprint import pformat

from typing import Union, Optional, Any, List

import edgeimpulse
import pydantic

from edgeimpulse.model.output_type import (
    Classification,
    Regression,
    ObjectDetection,
)
from edgeimpulse.model.input_type import (
    AudioInput,
    TimeSeriesInput,
    OtherInput,
)
from edgeimpulse.exceptions import (
    InvalidTargetException,
    InvalidEngineException,
    InvalidDeployParameterException,
    EdgeImpulseException,
    InvalidModelException,
)

from edgeimpulse.util import (
    configure_generic_client,
    poll,
    default_project_id_for,
    get_project_deploy_targets,
    upload_pretrained_model_and_data,
)
from edgeimpulse_api import JobsApi, DeploymentApi, LearnApi
from edgeimpulse_api.models.save_pretrained_model_request import (
    SavePretrainedModelRequest,
)
from edgeimpulse_api.models.build_on_device_model_request import (
    BuildOnDeviceModelRequest,
)
from edgeimpulse_api.models.deployment_target_engine import DeploymentTargetEngine
from edgeimpulse_api.models.keras_model_type_enum import KerasModelTypeEnum
from edgeimpulse_api.models.pretrained_model_tensor import PretrainedModelTensor


def deploy(
    model: Union[Path, str, bytes, Any],
    model_output_type: Union[Classification, Regression, ObjectDetection],
    model_input_type: Optional[Union[AudioInput, TimeSeriesInput, OtherInput]] = None,
    deploy_target: str = "zip",
    deploy_model_type: Optional[str] = None,
    engine: str = "tflite",
    representative_data_for_quantization: Optional[Union[Path, str, bytes, Any]] = None,
    output_directory: Optional[str] = None,
    api_key: Optional[str] = None,
) -> bytes:
    """
        Transforms a trained model into a library, package, or firmware ready to deploy on an embedded device. Can optionally
        apply post-training quantization if a representative data sample is uploaded.

        Supported model formats:
            * [Keras Model instance](https://www.tensorflow.org/api_docs/python/tf/keras/Model)
            * [TensorFlow SavedModel](https://www.tensorflow.org/guide/saved_model) (as path to directory or `.zip` file)
            * [ONNX model file](https://learn.microsoft.com/en-us/windows/ai/windows-ml/get-onnx-model) (as path to `.onnx` file)
            * [TensorFlow Lite file](https://www.tensorflow.org/lite/guide) (as bytes, or path to a file that is not `.zip` or `.onnx`)

        Use the `output_type` field to describe your model's type: classification, regression, etc.

        Use the `input_type` field to specify any input preprocessing (windowing, downsampling) that should be performed by the resulting library.

        Representative data:
            * Must be a numpy array or `.npy` file
            * Each element must have the same shape as your model's input
            * Must be representative of the range (maximum and minimum) of values in your training data.

    Args:
        model (Union[Path, str, bytes, Any]): Path object or str denoting file path to model, in memory bytes of the model or keras model object.
        model_output_type (Union[Classification, Regression, ObjectDetection]): model output class from edgeimpulse.model_info
        model_input_type (Union[AudioInput, TimeSeriesInput, OtherInput], optional): model input class from edgeimpuse.model_info. Defaults to None.
        deploy_target (str, optional): Target to deploy to, defaulting to a portable C++ library suitable for most devices. See `edgeimpulse.model.list_deployment_targets()` for a list.
        deploy_model_type (str, optional): Use `int8` to receive an 8-bit quantized model, `float32` for non-quantized. Defaults to None, in which case it will become `int8` if representative_data_for_quantization if provided and `float32` otherwise. For other values see `edgeimpulse.model.list_model_types()`.
        engine (str, optional): Inference engine. Either `tflite` (for TensorFlow Lite for Microcontrollers) or `tflite-eon` (for EON Compiler) to output a portable C++ library. For all engines, call `edgeimpulse.deploy.list_engines()`. Defaults to `tflite`.
        representative_data_for_quantization: A numpy representative input dataset. Accepts either an in memory numpy array or the Path/str filename of a np.save .npy file.
        output_directory (str, optional): Directory to write deployment artifact to. File name may vary depending on deployment type. Defaults to None in which case model will not be written to file.
        api_key (str, optional): The API key for an Edge Impulse project. This can also be set via the module-level variable `edgeimpulse.API_KEY`, or the env var `EI_API_KEY`.
    Raises:
        InvalidDeployParameterException: Unacceptable parameter given to deploy function
        InvalidTargetException: Unacceptable deploy_target  for this project.
        InvalidEngineException: Unacceptable engine for this target
    Returns:
        bytes: model deployment as bytes.
    """

    if model_input_type is None:
        model_input_type = OtherInput()

    if deploy_model_type is not None and deploy_model_type not in list_model_types():
        raise InvalidDeployParameterException(
            "deploy_model_type must be None, or one of the following:\n"
            f"{list_model_types()}\n"
            " If None and representative_data_for_quantization is specified,"
            " then int8 will be used, otherwise float32 is assumed."
        )

    if engine not in list_engines():
        raise InvalidEngineException(
            f"Engine '{engine}' is not valid. It must be one of the following:\n"
            f"{list_engines()}"
        )

    # create api and jobs client
    client = configure_generic_client(
        key=api_key if api_key else edgeimpulse.API_KEY,
        host=edgeimpulse.API_ENDPOINT,
    )

    # derive default project id for client
    project_id = default_project_id_for(client)

    # The API bindings currently require files to be on disk.
    # We will write files to this temporary dir if necessary.
    with tempfile.TemporaryDirectory() as tempdir:
        upload_pretrained_model_and_data(
            tempdir=tempdir,
            client=client,
            project_id=project_id,
            model=model,
            representative_data=representative_data_for_quantization,
        )

    learn = LearnApi(client)
    jobs = JobsApi(client)
    deploy = DeploymentApi(client)

    try:
        info = learn.get_pretrained_model_info(project_id=project_id)
        available_model_types = info.available_model_types
        if info.model is None:
            raise EdgeImpulseException(
                "get_pretrained_model_info did not return model details"
            )
        outputs = info.model.outputs
    except Exception as e:
        logging.debug(f"Exception fetching model info: [{str(e)}]")
        raise e

    deploy_model_type = determine_deploy_type(
        deploy_model_type=deploy_model_type,
        representative_data_for_quantization=representative_data_for_quantization,
        available_model_types=available_model_types,
    )

    model_output_type = determine_output_type(model_output_type=model_output_type, outputs=outputs)

    try:
        r = SavePretrainedModelRequest.from_dict(
            {"input": model_input_type, "model": model_output_type}
        )
        response = learn.save_pretrained_model_parameters(
            project_id=project_id, save_pretrained_model_request=r
        )
    except Exception as e:
        logging.debug(f"exception starting job for upload request [{str(e)}]")
        raise e

    # check deploy target is valid for this project
    target_names = get_project_deploy_targets(client)
    if deploy_target not in target_names:
        raise InvalidTargetException(deploy_target, target_names)

    try:
        request = BuildOnDeviceModelRequest.from_dict(
            {"engine": engine, "modelType": deploy_model_type}
        )
    except pydantic.error_wrappers.ValidationError as e:
        if "validation error for BuildOnDeviceModelRequest\nengine\n" in str(e):
            raise InvalidEngineException(e)
        raise e

    try:
        build_job = jobs.build_on_device_model_job(
            project_id=project_id,
            type=deploy_target,
            build_on_device_model_request=request,
        )
        job_id = build_job.id
    except Exception as e:
        logging.debug(f"exception starting job for build job request [{str(e)}]")
        raise e

    job_response = poll(
        jobs_client=jobs,
        project_id=project_id,
        job_id=job_id,
    )
    logging.info(job_response)

    # download deployed asset
    response = deploy.download_build(
        project_id=project_id,
        type=deploy_target,
        engine=engine,
        model_type=deploy_model_type,
        _preload_content=False,
    )
    logging.info(f"Deployment is {len(response.data)} bytes")

    # write, as binary, to specified file.
    # derive sensible name if none was provided
    if output_directory is not None:
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        d = response.headers["Content-Disposition"]
        output_filename = re.findall("filename\*?=(.+)", d)[0].replace("utf-8''", "")
        output_path = os.path.join(output_directory, output_filename)
        logging.info(f"Writing out to {output_path}")
        with open(output_path, "wb") as f:
            f.write(response.data)

    return response.data


def list_deployment_targets(api_key: Optional[str] = None) -> "List[str]":
    """Lists suitable deployment targets for the project associated with configured or provided api key.

    Args:
        api_key (str, optional): The API key for an Edge Impulse project. This can also be set via the module-level variable `edgeimpulse.API_KEY`.
    """
    client = configure_generic_client(
        key=api_key if api_key else edgeimpulse.API_KEY,
        host=edgeimpulse.API_ENDPOINT,
    )
    return get_project_deploy_targets(client)


def list_engines() -> "List[str]":
    """Lists all the engines that can be passed to `deploy()`'s `engine` parameter."""
    return [e.value for e in DeploymentTargetEngine]


def list_model_types() -> "List[str]":
    """Lists all the model types that can passed to `deploy()`'s `deploy_model_type` parameter."""
    return [t.value for t in KerasModelTypeEnum]


def determine_deploy_type(
    deploy_model_type: Optional[str],
    representative_data_for_quantization: Optional[Union[Path, str, bytes, Any]],
    available_model_types: List[KerasModelTypeEnum],
):
    if deploy_model_type is not None and deploy_model_type not in available_model_types:
        raise InvalidDeployParameterException(
            f"You specified a deploy_model_type of {deploy_model_type}, but "
            f"for this model only these are available:\n"
            f"{str(available_model_types)}"
        )

    # depending on whether a representative dataset has been provided we assume float32 or
    # switch to int8, but never clobber user requested one ( if provided )
    if representative_data_for_quantization is None:
        if deploy_model_type is None:
            logging.info(
                "Both representative_data_for_quantization &"
                " deploy_model_type are None so setting"
                " deploy_model_type to float32"
            )
            # We may have an int8 model
            if "float32" in available_model_types:
                deploy_model_type = "float32"
            else:
                if "int8" in available_model_types:
                    deploy_model_type = "int8"
                else:
                    raise InvalidDeployParameterException(
                        f"You did not specify a deploy_model_type and we "
                        "were unable to determine it automatically. Acceptable"
                        "values for this model are:\n"
                        f"{str(available_model_types)}"
                    )
    else:
        if deploy_model_type is None:
            logging.info(
                "Both representative_data_for_quantization provided &"
                " deploy_model_type is None so setting"
                " deploy_model_type to int8"
            )
            if "int8" in available_model_types:
                deploy_model_type = "int8"
            else:
                raise InvalidDeployParameterException(
                    f"You provided representative_data_for_quantization, "
                    "which implies an int8 deploy_model_type, but for this "
                    "model int8 is not available. Available types are:\n"
                    f"{str(available_model_types)}"
                )

    return deploy_model_type


def determine_output_type(
    model_output_type: Union[Classification, Regression, ObjectDetection],
    outputs: List[PretrainedModelTensor],
):
    # Validate the specified model output as much as possible
    if type(model_output_type) != ObjectDetection:
        if len(outputs) > 1:
            raise InvalidModelException(
                f"Expected {type(model_output_type)} model to have 1 "
                f"output but it has {len(outputs)}"
            )
        if len(outputs[0].shape) != 2:
            raise InvalidModelException(
                f"Expected {type(model_output_type)} model to have 2 output "
                f"dimensions but has {len(outputs[0].shape)}"
            )
        if type(model_output_type) == Regression:
            output_neurons = outputs[0].shape[1]
            if output_neurons > 1:
                raise InvalidModelException(
                    f"Expected Regression model to have scalar output but "
                    f"has vector with length {output_neurons}"
                )

    # Allow for setting the number of labels
    if type(model_output_type) == Classification:
        output_neurons = outputs[0].shape[1]
        if model_output_type["labels"] is None:
            logging.info(
                f"Setting labels to match model output length of {output_neurons}"
            )
            model_output_type["labels"] = [str(num) for num in range(output_neurons)]
        else:
            expected_neurons = len(model_output_type["labels"])
            if output_neurons != len(model_output_type["labels"]):
                raise InvalidDeployParameterException(
                    "You specified a Classification model with "
                    f"{expected_neurons} labels but the model has "
                    f"{output_neurons} labels."
                )

    return model_output_type
