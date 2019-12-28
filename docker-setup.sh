#! /bin/bash
# Download gurobi binaries into .private/
# Then run this file to create a docker image
docker build -t private/sage-gurobi -f - .private <<EOF
 # Image mkoeppe/conda-sagemath-coinor built by https://github.com/mkoeppe/sage-numerical-backends-coin/blob/master/.github/workflows/build.yml
FROM mkoeppe/conda-sagemath-coinor
ADD gurobi8.0.1_linux64.tar.gz /opt
ADD gurobi8.1.1_linux64.tar.gz /opt
ADD gurobi9.0.0_linux64.tar.gz /opt
# Adding a license key like this does not help because Gurobi licenses are keyed to a 'host id'.
# See https://stackoverflow.com/questions/58663540/gurobi-in-docker-container-problem-generating-unique-host-id-for-this-machine
# ADD gurobi.lic /root
EOF
