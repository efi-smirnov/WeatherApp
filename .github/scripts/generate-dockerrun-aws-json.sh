#!/bin/bash


# Get the Docker image tag (defaults to "latest" if not provided)
image_tag=$1
if [ -z "$image_tag" ]; then
  image_tag="latest"
fi

# DockerHub username and repository are passed as environment variables
docker_username=$2
if [ -z "$docker_username" ]; then
  echo "DockerHub username not provided"
  exit 1
fi

container_port=$3

# Generate the Dockerrun.aws.json file
echo "{
  \"AWSEBDockerrunVersion\": 1,
  \"Image\": {
    \"Name\": \"$docker_username/weather-app:$image_tag\",
    \"Update\": \"true\"
  },
  \"Ports\": [
    {
      \"ContainerPort\": \"$container_port\"
    }
  ]
}" > Dockerrun.aws.json

echo "Dockerrun.aws.json generated with Docker image: $docker_username/weather-app:$image_tag"