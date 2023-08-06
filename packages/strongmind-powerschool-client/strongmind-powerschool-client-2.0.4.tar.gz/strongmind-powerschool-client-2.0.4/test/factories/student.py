import json

import factory


class StudentFactory(factory.Factory):
    pass


SAMPLE_STUDENT_1 = json.loads("""
{
  "student": {
    "@expansions": "demographics, addresses, alerts, phones, school_enrollment, ethnicity_race, contact, contact_info, initial_enrollment, schedule_setup, fees, lunch",
    "@extensions": "s_az_stu_hir_x,s_stu_crdc_x,s_stu_x,c_studentlocator,s_az_stu_x,s_stu_ncea_x,s_stu_edfi_x,studentcorefields",
    "id": 156,
    "local_id": 10013,
    "student_username": "testuser123",
    "name": {
      "first_name": "Test",
      "middle_name": "Middle",
      "last_name": "Astudio8"
    },
    "demographics": {
      "gender": "M",
      "birth_date": "2001-01-02",
      "projected_graduation_year": 0
    },
    "addresses": {
      "physical": {
        "street": "",
        "state_province": "AZ"
      }
    },
    "alerts": "",
    "phones": {
      "main": {
        "number": 1234567890
      }
    },
    "school_enrollment": {
      "enroll_status": "A",
      "enroll_status_description": "Active",
      "enroll_status_code": 0,
      "grade_level": 6,
      "entry_date": "2020-02-11",
      "exit_date": "2020-05-27",
      "school_number": 101,
      "school_id": 53,
      "entry_code": "NONE",
      "district_of_residence": 100,
      "full_time_equivalency": {
        "fteid": 2,
        "name": "Full Time"
      }
    },
    "ethnicity_race": {
      "federal_ethnicity": "NO",
      "races": [
        {
          "district_race_code": "AS",
          "district_race_code_description": "Asian",
          "federal_race_code_category": "Asian"
        },
        {
          "district_race_code": "WH",
          "district_race_code_description": "White",
          "federal_race_code_category": "White"
        },
        {
          "district_race_code": "BL",
          "district_race_code_description": "Black or African American",
          "federal_race_code_category": "Black or African American"
        },
        {
          "district_race_code": "AM",
          "district_race_code_description": "American Indian or Alaska Native",
          "federal_race_code_category": "American Indian or Alaska Native"
        },
        {
          "district_race_code": "PI",
          "district_race_code_description": "Native Hawaiian / Other Pac Islander",
          "federal_race_code_category": "Native Hawaiian / Other Pac Islander"
        }
      ]
    },
    "contact": {
      "mother": "Snotter, Sue",
      "father": "Snotter, Harry"
    },
    "contact_info": {
      "email": "testuser123@notarealboy.com"
    },
    "initial_enrollment": {
      "district_entry_grade_level": 0,
      "school_entry_grade_level": 0
    },
    "schedule_setup": {
      "sched_next_year_grade": 0
    },
    "fees": "",
    "lunch": {
      "balance_1": "0.00",
      "balance_2": "0.00",
      "balance_3": "0.00",
      "balance_4": "0.00",
      "lunch_id": 0
    }
  }
}
""")

STUDENT_1_ONEROSTER_USER = json.loads("""
{
  "sourcedId": 10013,
  "status": "active",
  "dateLastModified": null,
  "metadata": {
    "https://schemas.strongmind.com/oneroster/completeness": true,
    "https://schemas.strongmind.com/oneroster/canvas_domain": "ventureinternational.strongmind.com",
    "https://schemas.strongmind.com/oneroster/partner_name": "venture",
    "https://schemas.strongmind.com/oneroster/self-guardian": false,
    "https://schemas.strongmind.com/oneroster/agent-data-access": [],
    "https://schemas.strongmind.com/oneroster/inline-objects": {}
  },
  "username": "testuser123",
  "userIds": [
    {
      "type": "powerschool_dcid",
      "identifier": "156"
    },
    {
      "type": "powerschool_number",
      "identifier": "10013"
    }
  ],
  "enabledUser": true,
  "givenName": "Test",
  "familyName": "Astudio8",
  "middleName": "Middle",
  "role": "student",
  "identifier": "testuser123 10013",
  "email": "testuser123@notarealboy.com",
  "sms": 1234567890,
  "phone": 1234567890,
  "agents": [],
  "orgs": 101,
  "grades": [
    "06"
  ],
  "password": null
}
""")

STUDENT_1_ONEROSTER_DEMOGRAPHICS = json.loads("""
{"sourcedId":10013,"status":"active","dateLastModified":null,"metadata":{"https://schemas.strongmind.com/oneroster/canvas_domain": "ventureinternational.strongmind.com","https://schemas.strongmind.com/oneroster/partner_name": "venture"},"birthDate":"2001-01-02","sex":"M","americanIndianOrAlaskaNative":true,"asian":true,"blackOrAfricanAmerican":true,"nativeHawaiianOrOtherPacificIslander":true,"white":true,"demographicRaceTwoOrMoreRaces":true}
""")

SAMPLE_STUDENT_2 = json.loads("""
{"student":{"@expansions":"demographics, addresses, alerts, phones, school_enrollment, ethnicity_race, contact, contact_info, initial_enrollment, schedule_setup, fees, lunch","@extensions":"s_az_stu_hir_x,s_stu_crdc_x,s_stu_x,c_studentlocator,s_az_stu_x,s_stu_ncea_x,s_stu_edfi_x,studentcorefields","id":157,"local_id":10014,"name":{"first_name":"Student","last_name":"Pav"},"student_username":"testname999","demographics":{"gender":"F","birth_date":"2003-02-12","projected_graduation_year":0},"addresses":{"physical":{"street":"","state_province":"AZ"}},"alerts":"","phones":"","school_enrollment":{"enroll_status":"A","enroll_status_description":"Active","enroll_status_code":0,"grade_level":6,"entry_date":"2020-02-14","exit_date":"2020-05-27","school_number":100,"school_id":3,"district_of_residence":100,"full_time_equivalency":{"fteid":2,"name":"Full Time"}},"ethnicity_race":{"scheduling_reporting_ethnicity":"W"},"contact_info":{"email": "a@b.c"},"initial_enrollment":{"district_entry_grade_level":0,"school_entry_grade_level":0},"schedule_setup":{"sched_next_year_grade":0},"fees":"","lunch":{"balance_1":"0.00","balance_2":"0.00","balance_3":"0.00","balance_4":"0.00","lunch_id":0}}}
""")

STUDENT_2_ONEROSTER_USER = json.loads("""
{
  "sourcedId": 10014,
  "status": "active",
  "dateLastModified": null,
  "metadata": {
    "https://schemas.strongmind.com/oneroster/completeness": true,
    "https://schemas.strongmind.com/oneroster/canvas_domain": "testschool.strongmind.com",
    "https://schemas.strongmind.com/oneroster/partner_name": "testschool",
    "https://schemas.strongmind.com/oneroster/self-guardian": false,
    "https://schemas.strongmind.com/oneroster/agent-data-access": [],
    "https://schemas.strongmind.com/oneroster/inline-objects": {}
  },
  "username": "testname999",
  "userIds": [
    {
      "type": "powerschool_dcid",
      "identifier": "157"
    },
    {
      "type": "powerschool_number",
      "identifier": "10014"
    }
  ],
  "enabledUser": true,
  "givenName": "Student",
  "familyName": "Pav",
  "middleName": null,
  "role": "student",
  "identifier": "testname999 10014",
  "email": null,
  "sms": null,
  "phone": null,
  "agents": [],
  "email": "a@b.c",
  "orgs": 100,
  "grades": [
    "06"
  ],
  "password": null
}
""")
STUDENT_2_ONEROSTER_DEMOGRAPHICS = json.loads("""
{"sourcedId":10014,"status":"active","dateLastModified":null,"metadata":{"https://schemas.strongmind.com/oneroster/canvas_domain": "testschool.strongmind.com", "https://schemas.strongmind.com/oneroster/partner_name": "testschool"},"birthDate":"2003-02-12","sex":"F"}
""")

SAMPLE_STUDENT_3 = json.loads("""
{"student":{"@expansions":"demographics, addresses, alerts, phones, school_enrollment, ethnicity_race, contact, contact_info, initial_enrollment, schedule_setup, fees, lunch","@extensions":"s_az_stu_hir_x,s_stu_crdc_x,s_stu_x,c_studentlocator,s_az_stu_x,s_stu_ncea_x,s_stu_edfi_x,studentcorefields","id":157,"local_id":10014,"name":{"first_name":"Student","last_name":"Pav"},"demographics":{"projected_graduation_year":0},"addresses":{"physical":{"street":"","state_province":"AZ"}},"alerts":"","phones":"","school_enrollment":{"enroll_status":"A","enroll_status_description":"Active","enroll_status_code":0,"grade_level":6,"entry_date":"2020-02-14","exit_date":"2020-05-27","school_number":101,"school_id":3,"district_of_residence":100,"full_time_equivalency":{"fteid":2,"name":"Full Time"}},"ethnicity_race":{"scheduling_reporting_ethnicity":"W","races":{"district_race_code":"WH","district_race_code_description":"White","federal_race_code_category":"White"}},"contact_info":{"email": "a@b.c"},"initial_enrollment":{"district_entry_grade_level":0,"school_entry_grade_level":0},"schedule_setup":{"sched_next_year_grade":0},"fees":"","lunch":{"balance_1":"0.00","balance_2":"0.00","balance_3":"0.00","balance_4":"0.00","lunch_id":0}}}
""")
