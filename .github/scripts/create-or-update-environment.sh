#!/bin/bash

# Parameters
app_name=$1 # Application name
environment_name=$2    # JIRA ticket ID (or branch name) used as the environment name
region=$3    # AWS region

if [ -z "$environment_name" ]; then
  echo "Environment name (JIRA ticket or branch) not provided"
  exit 1
fi

# Function to check the environment status
check_environment_status() {
  local status
  status=$(aws elasticbeanstalk describe-environments \
      --application-name "$app_name" \
      --environment-names "$environment_name" \
      --region "$region" \
      --query "Environments[0].Status" \
      --output text | cat)
  echo "$status"
}

# Check if the environment exists
existing_envs=$(aws elasticbeanstalk describe-environments \
  --application-name "$app_name" \
  --environment-names "$environment_name" \
  --region "$region" \
  --query "Environments[?EnvironmentName=='$environment_name']" \
  --output json | cat)

create_environment=false

if [ "$(echo "$existing_envs" | jq 'length')" -gt 0 ]; then
  status=$(echo "$existing_envs" | jq -r '.[0].Status')
  if [ "$status" == "Ready" ]; then
    echo "Environment '$environment_name' is Ready. Proceeding to deploy."
  elif [ "$status" == "Terminated" ]; then
    echo "Environment '$environment_name' is Terminated. Creating a new environment."
    create_environment=true
  else
    echo "Environment '$environment_name' is in status: $status. Proceeding with update."
  fi
else
  echo "Environment '$environment_name' does not exist. Creating a new environment."
  create_environment=true
fi

# Create the environment if it doesn't exist or is terminated
if [ "$create_environment" = true ]; then
  platform_arn=$(aws elasticbeanstalk list-platform-versions \
      --filters "Type=PlatformBranchName,Operator=begins_with,Values=Docker running on 64bit Amazon Linux 2023" \
      --query "PlatformSummaryList[0].PlatformArn" --output text --region "$region" | cat)

  aws elasticbeanstalk create-environment \
    --application-name "$app_name" \
    --environment-name "$environment_name" \
    --platform-arn "$platform_arn" \
    --option-settings file://options.json \
    --tier '{"Name":"WebServer","Type":"Standard"}' \
    --cname-prefix "$environment_name" \
    --region "$region"

  echo "Waiting for environment '$environment_name' to be ready..."
  max_attempts=20
  attempt=0
  while [ $attempt -lt $max_attempts ]; do
    sleep 30
    status=$(check_environment_status)
    echo "Current status: $status"
    if [ "$status" == "Ready" ]; then
      echo "Environment is Ready."
      break
    fi
    attempt=$((attempt + 1))
  done

  if [ "$status" != "Ready" ]; then
    echo "Environment did not become Ready in time."
    exit 1
  fi
fi

# Deploy the application to the environment
eb init "$app_name" --platform docker --region "$region"
eb deploy "$environment_name" --verbose

# Output URL
deployed_url=$(aws elasticbeanstalk describe-environments \
  --application-name "$app_name" \
  --environment-names "$environment_name" \
  --query "Environments[0].CNAME" --output text --region "$region" | cat)

echo "deployed_url=$deployed_url" >> $GITHUB_ENV