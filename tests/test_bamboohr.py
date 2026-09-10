import pytest
from include.sources.bamboohr import parse
import os
import json

fixture_file_path = os.path.join(os.path.dirname(__file__), "fixtures", "bamboohr_list.json")

# test the possible cases: one with location and atsLocation, and one with only location and one with only atsLocation
@pytest.mark.parametrize(
    "value,expected", [
        (    
            {
            "id": "389",
            "jobOpeningName": "Sales Engineer",
            "departmentId": "18687",
            "departmentLabel": "Pre-Sales",
            "employmentStatusLabel": "Full-Time",
            "employmentType": None,
            "location": {
                "city": "Frankfurt am Main",
                "state": "Hesse"
            },
            "atsLocation": {
                "country": None,
                "state": None,
                "province": None,
                "city": None
            },
            "isRemote": None,
            "locationType": "2"
            }, 
        [
            {
                "id": "389",
                "title": "Sales Engineer",
                "url": "https://iqgeo.bamboohr.com/careers/389",
                "location": "Frankfurt am Main, Hesse"
            }
        ]
        ),
        (
               {
      "id": "424",
      "jobOpeningName": "Technical Support Engineer",
      "departmentId": "18656",
      "departmentLabel": "Support",
      "employmentStatusLabel": "Full-Time",
      "employmentType": None,
      "location": {
        "city": None,
        "state": None
      },
      "atsLocation": {
        "country": "Japan",
        "state": None,
        "province": None,
        "city": None
      },
      "isRemote": None,
      "locationType": "1"
    },
      [
        {
                "id": "424",
                "title": "Technical Support Engineer",
                "url": "https://iqgeo.bamboohr.com/careers/424",
                "location": "Japan"
            }
        ]),
    ]
)
def test_parse(value, expected):
    class MockResponse:
        def json(self):
            return {"result": [value]}
    source = {
            "company": "IQGeo",
            "api_url": "https://iqgeo.bamboohr.com/careers/list",
            "state_file": "job_state_iqgeo.json",
            "ats": "bamboohr"
        }
    assert parse(MockResponse(), source) == expected
    