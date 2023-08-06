import os
import docker
from .fastapi import create_fastapi_file
from pureml.schema import FastAPISchema, PredictSchema, DockerSchema

prediction_schema = PredictSchema()
fastapi_schema = FastAPISchema()
docker_schema = DockerSchema()


def create_docker_file(org_id, access_token):
    # os.makedirs(PATH_DOCKER_DIR, exist_ok=True)
    os.makedirs(prediction_schema.paths.PATH_PREDICT_DIR, exist_ok=True)

    req_pos = prediction_schema.PATH_PREDICT_REQUIREMENTS.rfind(
        prediction_schema.paths.PATH_PREDICT_DIR_RELATIVE
    )
    req_path = prediction_schema.PATH_PREDICT_REQUIREMENTS[req_pos:]

    api_pos = fastapi_schema.PATH_FASTAPI_FILE.rfind(
        prediction_schema.paths.PATH_PREDICT_DIR_RELATIVE
    )
    api_path = fastapi_schema.PATH_FASTAPI_FILE[api_pos:]

    docker = """
    
FROM {BASE_IMAGE}

ENV ORG_ID={ORG_ID}
ENV ACCESS_TOKEN={ACCESS_TOKEN}

RUN mkdir -p {PREDICT_DIR}

WORKDIR {PREDICT_DIR}

ADD . {PREDICT_DIR}

COPY . .

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r {REQUIREMENTS_PATH}

RUN pip install fastapi uvicorn python-multipart

RUN pip install pureml

EXPOSE {PORT}
CMD ["python", "{API_PATH}"]    
""".format(
        BASE_IMAGE=docker_schema.BASE_IMAGE_DOCKER,
        PORT=docker_schema.PORT_DOCKER,
        PREDICT_DIR=prediction_schema.paths.PATH_PREDICT_DIR_RELATIVE,
        API_PATH=api_path,
        REQUIREMENTS_PATH=req_path,
        ORG_ID=org_id,
        ACCESS_TOKEN=access_token,
    )

    with open(docker_schema.PATH_DOCKER_IMAGE, "w") as docker_file:
        docker_file.write(docker)

    docker_yaml = """version: '3'

services:
  prediction:
    build: .
    container_name: "{CONTAINER_NAME}"
    expose:
      - "{DOCKER_PORT}"
    ports:
      - "{HOST_PORT}:{DOCKER_PORT}"
    
    """.format(
        DOCKER_PORT=docker_schema.PORT_DOCKER,
        HOST_PORT=docker_schema.PORT_HOST,
        CONTAINER_NAME="pureml_prediction",
    )

    with open(docker_schema.PATH_DOCKER_CONFIG, "w") as docker_yaml_file:
        docker_yaml_file.write(docker_yaml)


def create_docker_image(image_tag=None):
    if image_tag is None:
        image_tag = "pureml_docker_image"
    else:
        image_tag = image_tag.replace(" ", "")

        client = docker.from_env()

        docker_file_path_relative = docker_schema.PATH_DOCKER_IMAGE.split(os.path.sep)[
            -1
        ]

        try:
            image, build_log = client.images.build(
                path=docker_schema.paths.PATH_PREDICT_DIR,
                dockerfile=docker_file_path_relative,
                tag=image_tag,
                nocache=True,
                rm=True,
            )

            print("Docker image is created")
            print(image)

        except Exception as e:
            print(e)
            image = None

        return image


def run_docker_container(image, name):
    client = docker.from_env()

    docker_port = "{port}/tcp".format(port=docker_schema.PORT_DOCKER)
    # print(docker_port)

    container = client.containers.run(
        image=image,
        ports={docker_port: docker_schema.PORT_HOST},
        detach=True,
        name=name,
    )

    return container


def create(
    label,
    org_id,
    access_token,
    image_tag=None,
    predict_path=None,
    requirements_path=None,
    container_name=None,
):

    create_fastapi_file(
        label=label, predict_path=predict_path, requirements_path=requirements_path
    )

    create_docker_file(org_id=org_id, access_token=access_token)

    image = create_docker_image(image_tag)

    if image is not None:
        container = run_docker_container(image=image, name=container_name)

        print("Created Docker container")
        print(container)
        print(
            "Prediction requests can be forwarded to {ip}:{port}/predict".format(
                ip=docker_schema.API_IP_HOST, port=docker_schema.PORT_HOST
            )
        )
    else:
        print("Failed to create the container")


def get(container_id):

    client = docker.from_env()

    container = client.containers.get(container_id)

    return container


def stop(container_id):

    client = docker.from_env()

    container = client.containers.get(container_id)

    container.stop()
