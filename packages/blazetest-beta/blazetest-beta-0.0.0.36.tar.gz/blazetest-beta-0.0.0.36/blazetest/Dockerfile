FROM railflow/blazetest:PYTHON_VERSION

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy project files and tests
ADD . ${LAMBDA_TASK_ROOT}/
ADD .blazetest/tests_runner_handler ${LAMBDA_TASK_ROOT}/tests_runner_handler
COPY .blazetest/scripts/install_dependencies.sh /tmp/

# Install Python deps
RUN /usr/bin/bash /tmp/install_dependencies.sh

CMD ["tests_runner_handler.handler.run_tests"]