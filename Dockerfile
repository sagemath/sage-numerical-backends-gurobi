# Use image built by docker-setup.sh
FROM private/sage-gurobi
ARG GUROBI_VERSION=9.0.0
ADD . /sage-numerical-backends-gurobi/
RUN bash -l -c 'conda activate sagecoin; export GUROBI_HOME=/opt/gurobi$(echo ${GUROBI_VERSION} | sed -e "s/[.]//g;")/linux64; cd sage-numerical-backends-gurobi && sage setup.py test && sage -python -m pip install . && ./test_all.sh'
