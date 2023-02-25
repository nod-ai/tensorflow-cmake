#!/usr/bin/env bash

set -e

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
BIN_DIR="$(pwd)"

"$SCRIPT_DIR/../install-build-dependencies-ubuntu.sh"

TF_BIN_DIR="$BIN_DIR/tensorflow"
INSTALL_DIR="$BIN_DIR/install"
TEST_BIN_DIR="$BIN_DIR/test"

cmake \
    -S "$SCRIPT_DIR/.." \
    -B "$TF_BIN_DIR" \
    "-DCMAKE_INSTALL_PREFIX=$INSTALL_DIR" \
    -DTF_URL=https://github.com/tensorflow/tensorflow/archive/v2.12.0-rc0.tar.gz \
    -DTF_VERSION=2.12.0 \

cd "$TF_BIN_DIR"
cmake --build .
cmake --install .

cmake \
    -S "$SCRIPT_DIR/../test" \
    -B "$TEST_BIN_DIR" \
    "-DCMAKE_PREFIX_PATH=$INSTALL_DIR/lib/cmake/TensorflowCC" \
    "-DCMAKE_VERBOSE_MAKEFILE=ON"
cd "$TEST_BIN_DIR"
cmake --build .
./tensorflow_smoke_test
