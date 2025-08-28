#!/bin/bash

# Configuration
IMAGE_NAME="rendergit-mcp:latest"
CONTAINER_NAME="rendergit-mcp-service"
NETWORK_NAME="shared_net"

# Function to stop and remove the container
stop_container() {
    echo "Stopping and removing existing container..."
    if [ "$(docker ps -q -f name=^/${CONTAINER_NAME}$)" ]; then
        docker stop "${CONTAINER_NAME}"
    fi
    if [ "$(docker ps -aq -f status=exited -f name=^/${CONTAINER_NAME}$)" ]; then
        docker rm "${CONTAINER_NAME}"
    fi
    echo "Container stopped and removed."
}

# Function to build the Docker image
build_image() {
    echo "Building Docker image: ${IMAGE_NAME}"
    docker build -t "${IMAGE_NAME}" .
    echo "Image built successfully."
}

# Function to start the container
start_container() {
    echo "Starting container: ${CONTAINER_NAME}"
    docker run -d \
        --name "${CONTAINER_NAME}" \
        --network "${NETWORK_NAME}" \
        -v /opt/docker:/projects/docker \
        -v /mnt/backblaze:/projects/backblaze \
        "${IMAGE_NAME}"
    echo "Container started successfully."
}

# Main script logic
case "$1" in
    start)
        build_image
        stop_container
        start_container
        ;;
    stop)
        stop_container
        ;;
    restart)
        build_image
        stop_container
        start_container
        ;;
    build)
        build_image
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|build}"
        exit 1
        ;;
esac

exit 0
