import pytest


@pytest.fixture(scope="session")
def clinician_app():
    return "clinician"


@pytest.fixture(scope="session")
def patient_app():
    return "patient"
