#! /bin/bash

source env.sh

echo "Creating docker network"
if [[ -z $(docker network ls -q --filter 'name=edge_workshop') ]]; then
    docker network create edge_workshop
    echo "Docker network created."
else
    echo "Docker network already present."
fi

make register-node-policy