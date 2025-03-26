#!/bin/bash

set -euo pipefail

IMAGE_NAME="chipper-scrape"
NETWORK_NAME="chipper_network"
BASE_URL="http://localhost:21200"

OS_TYPE=$(uname -s)
if [[ "$OS_TYPE" == *"MINGW"* || "$OS_TYPE" == *"MSYS"* ]]; then
    export MSYS_NO_PATHCONV=1
    echo "Detected Windows environment. Setting MSYS_NO_PATHCONV=1 to avoid path conversion issues."
fi

export CONTAINER_ENGINE
detect_container_engine() {
    if [ -n "${CONTAINER_ENGINE:-}" ]; then
        echo "Using container engine from environment: $CONTAINER_ENGINE"
    elif command -v podman &> /dev/null; then
        CONTAINER_ENGINE="podman"
        echo "Auto-detected container engine: $CONTAINER_ENGINE"
    elif command -v docker &> /dev/null; then
        CONTAINER_ENGINE="docker"
        echo "Auto-detected container engine: $CONTAINER_ENGINE"
    else
        echo "Error: No container engine (Docker or Podman) found."
        exit 1
    fi
}

build_image() {
    echo "Building image: $IMAGE_NAME"
    $CONTAINER_ENGINE build -t $IMAGE_NAME .
}

parse_args() {
    if [ $# -eq 0 ]; then
        echo "Usage: $0 URL [additional arguments...]"
        exit 1
    fi

    if [ "$1" == "--help" ]; then
        $CONTAINER_ENGINE run --rm --name ${IMAGE_NAME} ${IMAGE_NAME} --help
        exit 0
    fi

    URL="$1"
    shift
}

run_container() {
    local run_opts=(
        --rm
        --name "${IMAGE_NAME}"
        -v "${PWD}/output:/app/data:z"
        --network="$NETWORK_NAME"
        "${IMAGE_NAME}"
        --base-url="${BASE_URL}"
        "$URL"
    )

    $CONTAINER_ENGINE run "${run_opts[@]}" "$@"
}

detect_container_engine
build_image
parse_args "$@"
run_container "${@:1}"
