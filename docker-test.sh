#! /bin/bash
# First run ./docker-setup.sh
set -e
for v in 8.0.1 8.1.1 9.0.0; do
    docker build --build-arg GUROBI_VERSION=$v -t private/sage-gurobi-$v .
done
