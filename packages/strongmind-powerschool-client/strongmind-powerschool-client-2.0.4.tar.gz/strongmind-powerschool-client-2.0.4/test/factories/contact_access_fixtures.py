import json
STUDENT_GET_RESULT_1 = json.loads("""
{
    "student": {
        "@expansions": "demographics, addresses, alerts, phones, school_enrollment, ethnicity_race, contact, contact_info, initial_enrollment, schedule_setup, fees, lunch",
        "@extensions": "s_az_stu_hir_x,u_postgraduation,s_stu_crdc_x,s_stu_x,activities,c_studentlocator,s_az_stu_x,s_stu_ncea_x,s_stu_edfi_x,studentcorefields",
        "id": 1,
        "local_id": 10004,
        "student_username": "Luke.Skywalker10004",
        "name": {
            "first_name": "Luke",
            "last_name": "Skywalker"
        },
        "demographics": {
            "projected_graduation_year": 0
        },
        "addresses": {
            "physical": {
                "street": "",
                "state_province": "AZ"
            }
        },
        "alerts": "",
        "phones": "",
        "school_enrollment": {
            "enroll_status": "A",
            "enroll_status_description": "Active",
            "enroll_status_code": 0,
            "grade_level": 6,
            "entry_date": "2020-05-01",
            "exit_date": "2021-05-02",
            "school_number": 100,
            "school_id": 3,
            "full_time_equivalency": {
                "fteid": 3,
                "name": "Full Time"
            }
        },
        "ethnicity_race": {
            "scheduling_reporting_ethnicity": "W"
        },
        "contact": {
            "emergency_contact_name1": "Lars, Owen"
        },
        "contact_info": {
             "email": "luke@skywalker.com"
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
CONTACT_ACCESS_QUERY_RESULT_1 = json.loads("""
{
    "record": [
        {
            "studentcontactdetailid": "50",
            "student_dcid": "1",
            "contact_id": "101",
            "startdate": "2020-05-01",
            "student_first_name": "Luke",
            "contact_phonenumber_ispreferred": "0",
            "contact_last_name": "Lars",
            "contact_first_name": "Owen",
            "guardianpersonassocid": "50",
            "contact_email": "test2@test.com",
            "student_last_name": "Skywalker",
            "guardianid": "500000",
            "contact_phonenumber_issms": "0",
            "contact_phonenumberext": "4",
            "studentcontactassocid": "50",
            "enddate": "2020-05-17",
            "student_number": "10004",
            "contact_phonenumber": "5555555555",
            "contact_phonenumber_type": "Mobile",
            "guardianstudentid": "502522",
            "contact_dcid": "51",
            "has_data_access": "1",
            "relation_type": "guardian"
        },
        {
            "studentcontactdetailid": "5076",
            "student_dcid": "1",
            "contact_id": "651",
            "startdate": "2020-06-01",
            "student_first_name": "Luke",
            "contact_last_name": "Kenobi",
            "contact_first_name": "Obi",
            "guardianpersonassocid": "5050",
            "contact_email": "test2@test.com",
            "student_last_name": "Skywalker",
            "guardianid": "505000",
            "studentcontactassocid": "5076",
            "enddate": "2020-09-09",
            "student_number": "10004",
            "contact_dcid": "601",
            "has_data_access": "0",
            "relation_type": "guardian"
        },
        {
            "studentcontactdetailid": "5086",
            "student_dcid": "1",
            "contact_id": "102",
            "student_first_name": "Luke",
            "contact_email": "test3@test.strongmind.com",
            "contact_phonenumber_ispreferred": "1",
            "contact_last_name": "Skywalker",
            "contact_first_name": "Anakin",
            "guardianpersonassocid": "51",
            "student_last_name": "Skywalker",
            "guardianid": "500001",
            "contact_phonenumber_issms": "0",
            "contact_phonenumberext": "3",
            "studentcontactassocid": "5086",
            "student_number": "10004",
            "contact_phonenumber": "4805558886",
            "contact_phonenumber_type": "Not Set",
            "guardianstudentid": "505033",
            "contact_dcid": "52",
            "has_data_access": "1",
            "relation_type": "guardian"
        },
        {
            "studentcontactdetailid": "5086",
            "student_dcid": "1",
            "contact_id": "102",
            "student_first_name": "Luke",
            "contact_email": "test3@test.strongmind.com",
            "contact_phonenumber_ispreferred": "0",
            "contact_last_name": "Skywalker",
            "contact_first_name": "Anakin",
            "guardianpersonassocid": "51",
            "student_last_name": "Skywalker",
            "guardianid": "500001",
            "contact_phonenumber_issms": "1",
            "studentcontactassocid": "5086",
            "student_number": "10004",
            "contact_phonenumber": "5558888999",
            "contact_phonenumber_type": "Home",
            "guardianstudentid": "505033",
            "contact_dcid": "52",
            "has_data_access": "1",
            "relation_type": "guardian"
        },
        {
            "studentcontactdetailid": "2555",
            "student_dcid": "1",
            "contact_id": "101",
            "startdate": "2020-05-18",
            "student_first_name": "Luke",
            "contact_phonenumber_ispreferred": "0",
            "contact_last_name": "Lars",
            "contact_first_name": "Owen",
            "guardianpersonassocid": "50",
            "contact_email": "test2@test.com",
            "student_last_name": "Skywalker",
            "guardianid": "500000",
            "contact_phonenumber_issms": "0",
            "contact_phonenumberext": "4",
            "studentcontactassocid": "50",
            "enddate": "2020-06-08",
            "student_number": "10004",
            "contact_phonenumber": "5555555555",
            "contact_phonenumber_type": "Mobile",
            "guardianstudentid": "502522",
            "contact_dcid": "51",
            "has_data_access": "1",
            "relation_type": "guardian"
        }
    ],
    "@extensions": ""
}
""")
CONTACT_ACCESS_QUERY_RESULT_2 = json.loads("""
{
    "record": [
        {
            "studentcontactdetailid": "50",
            "student_dcid": "1",
            "contact_id": "101",
            "startdate": "2020-05-01",
            "student_first_name": "Luke",
            "contact_phonenumber_ispreferred": "0",
            "contact_last_name": "Lars",
            "contact_first_name": "Owen",
            "contact_email": "test2@test.com",
            "guardianpersonassocid": "50",
            "student_last_name": "Skywalker",
            "guardianid": "500000",
            "contact_phonenumber_issms": "0",
            "contact_phonenumberext": "4",
            "studentcontactassocid": "50",
            "enddate": "2020-05-17",
            "student_number": "10004",
            "contact_phonenumber": "5555555555",
            "contact_phonenumber_type": "Mobile",
            "guardianstudentid": "502522",
            "contact_dcid": "51",
            "has_data_access": "1",
            "relation_type": "guardian"
        },
        {
            "studentcontactdetailid": "5076",
            "student_dcid": "1",
            "contact_id": "651",
            "startdate": "2020-06-01",
            "contact_email": "test2@test.com",
            "student_first_name": "Luke",
            "contact_last_name": "Kenobi",
            "contact_first_name": "Obi",
            "guardianpersonassocid": "5050",
            "student_last_name": "Skywalker",
            "guardianid": "505000",
            "studentcontactassocid": "5076",
            "enddate": "2020-09-09",
            "student_number": "10004",
            "contact_dcid": "601",
            "has_data_access": "0",
            "relation_type": "guardian"
        },
        {
            "studentcontactdetailid": "5086",
            "student_dcid": "1",
            "contact_id": "102",
            "student_first_name": "Luke",
            "contact_email": "test3@test.strongmind.com",
            "contact_phonenumber_ispreferred": "1",
            "contact_last_name": "Skywalker",
            "contact_first_name": "Anakin",
            "guardianpersonassocid": "51",
            "student_last_name": "Skywalker",
            "guardianid": "500001",
            "contact_phonenumber_issms": "0",
            "contact_phonenumberext": "3",
            "studentcontactassocid": "5086",
            "student_number": "10004",
            "contact_phonenumber": "4805558886",
            "contact_phonenumber_type": "Not Set",
            "guardianstudentid": "505033",
            "contact_dcid": "52",
            "has_data_access": "1",
            "relation_type": "guardian"
        },
        {
            "studentcontactdetailid": "5086",
            "student_dcid": "1",
            "contact_id": "102",
            "student_first_name": "Luke",
            "contact_email": "test3@test.strongmind.com",
            "contact_phonenumber_ispreferred": "1",
            "contact_last_name": "Skywalker",
            "contact_first_name": "Anakin",
            "guardianpersonassocid": "51",
            "student_last_name": "Skywalker",
            "guardianid": "500001",
            "contact_phonenumber_issms": "1",
            "studentcontactassocid": "5086",
            "student_number": "10004",
            "contact_phonenumber": "5558888999",
            "contact_phonenumber_type": "Home",
            "guardianstudentid": "505033",
            "contact_dcid": "52",
            "has_data_access": "1",
            "relation_type": "guardian"
        },
        {
            "studentcontactdetailid": "2555",
            "student_dcid": "1",
            "contact_id": "101",
            "startdate": "2020-05-18",
            "student_first_name": "Luke",
            "contact_phonenumber_ispreferred": "0",
            "contact_last_name": "Lars",
            "contact_first_name": "Owen",
            "guardianpersonassocid": "50",
            "student_last_name": "Skywalker",
            "contact_email": "test2@test.com",
            "guardianid": "500000",
            "contact_phonenumber_issms": "0",
            "contact_phonenumberext": "4",
            "studentcontactassocid": "50",
            "enddate": "2020-06-08",
            "student_number": "10004",
            "contact_phonenumber": "5555555555",
            "contact_phonenumber_type": "Mobile",
            "guardianstudentid": "502522",
            "contact_dcid": "51",
            "has_data_access": "1",
            "relation_type": "guardian"
        }
    ],
    "@extensions": ""
}
""")

CONTACT_ACCESS_QUERY_RESULT_3 = json.loads("""
{
    "record": [
        {
            "studentcontactdetailid": "50",
            "student_dcid": "1",
            "student_last_name": "Skywalker",
            "guardianid": "500000",
            "contact_id": "101",
            "startdate": "2020-05-01",
            "student_first_name": "Luke",
            "contact_email": "test2@test.com",
            "studentcontactassocid": "50",
            "enddate": "2020-05-17",
            "student_number": "10004",
            "contact_last_name": "Lars",
            "contact_dcid": "51",
            "contact_first_name": "Owen",
            "has_data_access": "0",
            "guardianpersonassocid": "50",
            "relation_type": "guardian"
        },
        {
            "studentcontactdetailid": "2553",
            "student_dcid": "1",
            "student_last_name": "Skywalker",
            "guardianid": "502500",
            "contact_id": "354",
            "student_first_name": "Luke",
            "contact_email": "test2@test.com",
            "studentcontactassocid": "2553",
            "student_number": "10004",
            "contact_last_name": "Skywalker",
            "contact_dcid": "304",
            "contact_first_name": "Padme",
            "has_data_access": "0",
            "guardianpersonassocid": "2550",
            "relation_type": "guardian"
        },
        {
            "studentcontactdetailid": "51",
            "student_dcid": "1",
            "student_last_name": "Skywalker",
            "guardianid": "500001",
            "contact_id": "102",
            "student_first_name": "Luke",
            "contact_email": "test2@test.com",
            "studentcontactassocid": "51",
            "student_number": "10004",
            "guardianstudentid": "502508",
            "contact_last_name": "Skywalker",
            "contact_dcid": "52",
            "contact_first_name": "Anakin",
            "has_data_access": "1",
            "guardianpersonassocid": "51",
            "relation_type": "guardian"
        },
        {
            "studentcontactdetailid": "2555",
            "student_dcid": "1",
            "student_last_name": "Skywalker",
            "guardianid": "500000",
            "contact_id": "101",
            "startdate": "2020-05-18",
            "student_first_name": "Luke",
            "contact_email": "test2@test.com",
            "studentcontactassocid": "50",
            "enddate": "2020-05-31",
            "student_number": "10004",
            "contact_last_name": "Lars",
            "contact_dcid": "51",
            "contact_first_name": "Owen",
            "has_data_access": "0",
            "guardianpersonassocid": "50",
            "relation_type": "guardian"
        }
    ],
    "@extensions": ""
}
""")
CONTACT_ACCESS_QUERY_RESULT_4 = json.loads("""
{
    "record": [
        {
            "studentcontactdetailid": "50",
            "student_dcid": "1",
            "student_last_name": "Skywalker",
            "guardianid": "500000",
            "contact_id": "101",
            "startdate": "2020-05-01",
            "student_first_name": "Luke",
            "contact_email": "",
            "studentcontactassocid": "50",
            "enddate": "2020-05-17",
            "student_number": "10004",
            "contact_last_name": "Lars",
            "contact_dcid": "51",
            "contact_first_name": "Owen",
            "has_data_access": "0",
            "guardianpersonassocid": "50",
            "relation_type": "guardian"
        }
    ],
    "@extensions": ""
}
""")
CONTACT_ACCESS_QUERY_RESULT_5 = json.loads("""
{
    "record": [
        {
            "studentcontactdetailid": "50",
            "student_dcid": "1",
            "student_last_name": "Skywalker",
            "guardianid": "500000",
            "contact_id": "101",
            "startdate": "2020-05-01",
            "student_first_name": "Luke",
            "contact_email": "test@test.com",
            "studentcontactassocid": "50",
            "enddate": "2020-05-17",
            "student_number": "10004",
            "contact_last_name": "Lars",
            "contact_dcid": "51",
            "contact_first_name": "Owen",
            "has_data_access": "0",
            "guardianpersonassocid": "50",
            "relation_type": "Self"
        }
    ],
    "@extensions": ""
}
""")

CONTACT_ACCESS_QUERY_RESULT_NO_PRIMARY_EMAIL = json.loads("""
{
    "record": [
        {
            "studentcontactdetailid": "50",
            "student_dcid": "1",
            "student_last_name": "Skywalker",
            "guardianid": "500000",
            "contact_id": "101",
            "student_first_name": "Luke",
            "contact_email": "owen1@test.com",
            "studentcontactassocid": "50",
            "student_number": "10004",
            "contact_last_name": "Lars",
            "contact_dcid": "51",
            "contact_first_name": "Owen",
            "has_data_access": "0",
            "guardianpersonassocid": "50",
            "relation_type": "guardian",
            "isprimaryemailaddress": "0"
        },
        {
            "studentcontactdetailid": "2555",
            "student_dcid": "1",
            "student_last_name": "Skywalker",
            "guardianid": "500000",
            "contact_id": "101",
            "student_first_name": "Luke",
            "contact_email": "owen@gmail.com",
            "studentcontactassocid": "50",
            "student_number": "10004",
            "contact_last_name": "Lars",
            "contact_dcid": "51",
            "contact_first_name": "Owen",
            "has_data_access": "0",
            "guardianpersonassocid": "50",
            "relation_type": "guardian",
            "isprimaryemailaddress": "0"
        }
    ],
    "@extensions": ""
}
""")

CONTACT_ACCESS_QUERY_RESULT_MULTIPLE_EMAILS = json.loads("""
{
    "record": [
        {
            "studentcontactdetailid": "50",
            "student_dcid": "1",
            "student_last_name": "Skywalker",
            "guardianid": "500000",
            "contact_id": "101",
            "student_first_name": "Luke",
            "contact_email": "owen1@test.com",
            "studentcontactassocid": "50",
            "student_number": "10004",
            "contact_last_name": "Lars",
            "contact_dcid": "51",
            "contact_first_name": "Owen",
            "has_data_access": "0",
            "guardianpersonassocid": "50",
            "relation_type": "guardian",
            "isprimaryemailaddress": "0"
        },
        {
            "studentcontactdetailid": "2555",
            "student_dcid": "1",
            "student_last_name": "Skywalker",
            "guardianid": "500000",
            "contact_id": "101",
            "student_first_name": "Luke",
            "contact_email": "owen@gmail.com",
            "studentcontactassocid": "50",
            "student_number": "10004",
            "contact_last_name": "Lars",
            "contact_dcid": "51",
            "contact_first_name": "Owen",
            "has_data_access": "0",
            "guardianpersonassocid": "50",
            "relation_type": "guardian",
            "isprimaryemailaddress": "1"
        }
    ],
    "@extensions": ""
}
""")
CONTACT_ACCESS_QUERY_RESULT_MULTIPLE_EMAILS_AND_PHONE_NUMBERS = json.loads("""
{
    "record": [
        {
            "studentcontactdetailid": "50",
            "student_dcid": "1",
            "student_last_name": "Skywalker",
            "guardianid": "500000",
            "contact_id": "101",
            "student_first_name": "Luke",
            "contact_email": "owen1@test.com",
            "studentcontactassocid": "50",
            "student_number": "10004",
            "contact_last_name": "Lars",
            "contact_dcid": "51",
            "contact_first_name": "Owen",
            "has_data_access": "0",
            "guardianpersonassocid": "50",
            "relation_type": "guardian",
            "isprimaryemailaddress": "1",
            "contact_phonenumber": "5555555555",
            "contact_phonenumber_ispreferred": "0"
        },
        {
            "studentcontactdetailid": "2555",
            "student_dcid": "1",
            "student_last_name": "Skywalker",
            "guardianid": "500000",
            "contact_id": "101",
            "student_first_name": "Luke",
            "contact_email": "owen2@test.com",
            "studentcontactassocid": "50",
            "student_number": "10004",
            "contact_last_name": "Lars",
            "contact_dcid": "51",
            "contact_first_name": "Owen",
            "has_data_access": "0",
            "guardianpersonassocid": "50",
            "relation_type": "guardian",
            "isprimaryemailaddress": "0",
            "contact_phonenumber": "5555555555",
            "contact_phonenumber_ispreferred": "0"
        },
        {
            "studentcontactdetailid": "50",
            "student_dcid": "1",
            "student_last_name": "Skywalker",
            "guardianid": "500000",
            "contact_id": "101",
            "student_first_name": "Luke",
            "contact_email": "owen1@test.com",
            "studentcontactassocid": "50",
            "student_number": "10004",
            "contact_last_name": "Lars",
            "contact_dcid": "51",
            "contact_first_name": "Owen",
            "has_data_access": "0",
            "guardianpersonassocid": "50",
            "relation_type": "guardian",
            "isprimaryemailaddress": "1",
            "contact_phonenumber": "4444444444",
            "contact_phonenumber_ispreferred": "1"
        },
        {
            "studentcontactdetailid": "2555",
            "student_dcid": "1",
            "student_last_name": "Skywalker",
            "guardianid": "500000",
            "contact_id": "101",
            "student_first_name": "Luke",
            "contact_email": "owen2@test.com",
            "studentcontactassocid": "50",
            "student_number": "10004",
            "contact_last_name": "Lars",
            "contact_dcid": "51",
            "contact_first_name": "Owen",
            "has_data_access": "0",
            "guardianpersonassocid": "50",
            "relation_type": "guardian",
            "isprimaryemailaddress": "0",
            "contact_phonenumber": "4444444444",
            "contact_phonenumber_ispreferred": "1"
        }
    ],
    "@extensions": ""
}
""")