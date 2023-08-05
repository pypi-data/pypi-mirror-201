import datetime
import threading
import time

import pytest
import qiskit

import bluequbit

NUM_PER_THREAD = 3
NUM_THREADS = 3

qc_qiskit = qiskit.QuantumCircuit(2)
qc_qiskit.h(0)
qc_qiskit.x(1)

job_ids = [[] for _ in range(NUM_THREADS)]


def submit_task(dq_client, thread_no):
    for _ in range(NUM_PER_THREAD):
        job_ids[thread_no].append(dq_client.run(qc_qiskit, asynchronous=True).job_id)


@pytest.mark.timeout(120)
def test_stress_submit_jobs():
    dq_client = bluequbit.BQClient()
    time_now = datetime.datetime.now(datetime.timezone.utc)
    threads = []
    for i in range(NUM_THREADS):
        threads.append(
            threading.Thread(
                target=submit_task,
                args=(
                    dq_client,
                    i,
                ),
            )
        )
        threads[-1].start()

    for i in range(NUM_THREADS):
        threads[i].join()

    job_ids_flat = [item for sublist in job_ids for item in sublist]

    assert len(job_ids_flat) == NUM_THREADS * NUM_PER_THREAD

    completed = None
    for i in range(NUM_PER_THREAD * NUM_THREADS):
        completed = 0
        jobs = dq_client.search(
            created_later_than=time_now - datetime.timedelta(seconds=10)
        )
        for job_result in jobs:
            if (
                job_result.job_id in job_ids_flat
                and job_result.run_status == "COMPLETED"
                and job_result.error_message is None
            ):
                completed += 1
        print("Try", i, ". Num completed", completed)
        if completed == len(job_ids_flat):
            break
        time.sleep(5.0)

    assert completed == len(job_ids_flat)
