import os

import numpy as np
import pytest
import qiskit

import bluequbit

qc_qiskit = qiskit.QuantumCircuit(2)
qc_qiskit.h(0)
qc_qiskit.x(1)


def test_basic_cancel_job():
    dq_client = bluequbit.BQClient()

    jobs = []
    num_jobs = 5
    for _ in range(num_jobs):
        jobs.append(dq_client.run(qc_qiskit, asynchronous=True))

    dq_client.cancel(jobs[-1].job_id)

    for job in jobs[:-1]:
        res = dq_client.wait(job.job_id)
        assert res.run_status == "COMPLETED"
        assert res.error_message is None

    with pytest.raises(bluequbit.exceptions.BQJobNotCompleteError) as e_info:
        dq_client.wait(jobs[-1].job_id)
    assert e_info.value.run_status == "CANCELED"


@pytest.mark.skipif(
    "BLUEQUBIT_STRESS_TESTS" not in os.environ, reason="Requires env variable to be set"
)
def test_long_running_cancel_job():
    dq_client = bluequbit.BQClient()
    num_qubits = 29
    qc_qiskit = qiskit.QuantumCircuit(num_qubits)
    qc_qiskit.x(np.arange(num_qubits))

    r = dq_client.run(qc_qiskit, asynchronous=True)
    for _ in range(1200):
        res = dq_client.get(r.job_id)
        if res.run_status == "RUNNING":
            break
    else:
        raise AssertionError()

    r = dq_client.cancel(r.job_id)
    assert r.run_status == "CANCELED"
    assert r.error_message == "Canceled by user"
