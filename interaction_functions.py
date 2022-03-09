import json
import logging
import os

import stickytape
from qiskit import Aer
from qiskit.providers.ibmq.runtime import UserMessenger, RuntimeEncoder, RuntimeDecoder
from qiskit.providers.ibmq.runtime.exceptions import RuntimeProgramNotFound

from runtime_helpers.stickytape_overrides import _generate_module_writers

stickytape._generate_module_writers = _generate_module_writers

logger = logging.getLogger(__name__)


def _interim_result_callback(job_id, interim_result):
    logger.info(f"{job_id}: {interim_result}")


def local_test(run_time_program, inputs):
    backend = Aer.get_backend('qasm_simulator')
    user_messenger = UserMessenger()
    serialized_inputs = json.dumps(inputs, cls=RuntimeEncoder)
    deserialized_inputs = json.loads(serialized_inputs, cls=RuntimeDecoder)

    run_time_program.main(backend, user_messenger, **deserialized_inputs)


def build_program(path_program, python_paths=None):
    return stickytape.script(path_program, add_python_paths=python_paths)


def upload_program(provider, data=None, data_file=None, meta_data=None, meta_data_file=None):
    if data is None and data_file is not None:
        data = os.path.join(os.getcwd(), data_file)

    if meta_data is None and meta_data_file is not None:
        meta_data = os.path.join(os.getcwd(), meta_data_file)

    program_id = provider.runtime.upload_program(
        data=data,
        metadata=meta_data
    )
    logger.info(program_id)
    return program_id


def call_program(provider, program_id, options, inputs):
    job = provider.runtime.run(program_id=program_id,
                               options=options,
                               inputs=inputs,
                               callback=_interim_result_callback)
    logger.info(f"job ID: {job.job_id()}")
    return job.result()


def start_program(provider, program_id, options, inputs):
    job = provider.runtime.run(program_id=program_id,
                               options=options,
                               inputs=inputs,
                               callback=_interim_result_callback)
    logger.info(f"job ID: {job.job_id()}")
    return job


def delete_program(provider, program_id):
    provider.runtime.delete_program(program_id)


def delete_all_programs(provider):
    for program in provider.runtime.programs(refresh=True):
        try:
            delete_program(provider, program.program_id)
        except RuntimeProgramNotFound:
            pass
