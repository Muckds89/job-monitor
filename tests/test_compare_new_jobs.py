import pytest
from include.state import compare_new_jobs

JOB_A = {
        "id": "389",
        "title": "Sales Engineer",
        "url": "https://iqgeo.bamboohr.com/careers/389",
        "location": "Frankfurt am Main, Hesse"
    }
JOB_B = {
        "id": "390",
        "title": "Sales Engineer II",
        "url": "https://iqgeo.bamboohr.com/careers/390",
        "location": "Frankfurt am Oder"
    }

@pytest.mark.parametrize(
    "state,fetched,expected", 
    [
        ([JOB_A],[JOB_A,JOB_B],[JOB_B]),
        ([JOB_A, JOB_B],[JOB_A,JOB_B],[]),
        ([],[JOB_A,JOB_B],[JOB_A,JOB_B])
    ]
)
def test_compare_new_jobs(state,fetched,expected):
    assert compare_new_jobs(state,fetched) == expected