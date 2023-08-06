import json
from copy import deepcopy

import factory

from test.factories.student import SAMPLE_STUDENT_1

SAMPLE_POWERSCHOOL_INSERT_STUDENT_SUCCESS = json.loads("""
{
   "results":{
      "update_count":2,
      "result":[
         {
            "client_uid":124,
            "status":"SUCCESS",
            "action":"INSERT",
            "success_message":{
               "id":442,
               "ref":"https://server/ws/v1/student/442"
            }
         },
         {
            "client_uid":1245,
            "status":"SUCCESS",
            "action":"INSERT",
            "success_message":{
               "id":443,
               "ref":"https://server/ws/v1/student/443"
            }
         }
      ]
   }
}
""")

SAMPLE_POWERSCHOOL_INSERT_STUDENT_ERROR = json.loads("""
{
   "results":{
      "update_count":2,
      "result":[
         {
            "client_uid":1245,
            "status":"ERROR",
            "action":"INSERT",
            "error_message":{
               "error": [
               {
                  "field": "student/school_enrollment/entry_date",
                  "error_code": "REQUIRED",
                  "error_description": "No data submitted for required element"
               },
               {
                  "field": "student/school_enrollment/exit_date",
                  "error_code": "REQUIRED",
                  "error_description": "No data submitted for required element"
               },
               {
                  "field": "student/school_enrollment/school_number",
                  "error_code": "FIELD_VALIDATION_ERROR",
                  "error_description": "Value must be an integer"
               },
               {
                  "field": "student/school_enrollment/school_number",
                  "error_code": "FIELD_VALIDATION_ERROR",
                  "error_description": "Value must be a number"
               },
               {
                  "field": "student/school_enrollment/school_number",
                  "error_code": "FIELD_VALIDATION_ERROR",
                  "error_description": "Value may not contain more than 10 character(s)."
               }
               ]
            }
         }
      ]
   }
}
""")

SAMPLE_POWERSCHOOL_INSERT_STUDENT_SINGLE_WARNING = json.loads("""
{
   "results": {
      "delete_count": 0,
      "insert_count": 1,
      "result": {
         "action": "INSERT",
         "client_uid": 100,
         "status": "WARNING",
         "success_message": {
            "id": 501,
            "ref": "https://ventureinternational.powerschool.com/ws/v1/student/501"
         },
         "warning_message": {
            "warning": {
               "field": "student/fees",
               "warning_code": "FEES_ASSIGN_FEES_FAILED",
               "warning_description": "Fees assessment for this student failed for unknown reason."
            }
         }
      },
      "update_count": 0
   }
}
""")

POWERSCHOOL_API_SAMPLE_SECTION_ENROLLMENT = json.loads("""
{
   "section_enrollment": {
      "@extensions": "s_az_cc_x,s_cc_x,s_cc_edfi_x",
      "id": 962,
      "section_id": 51,
      "student_id": 569,
      "entry_date": "2020-05-01",
      "exit_date": "2020-07-01",
      "dropped": false
   }
}
""")

POWERSCHOOL_API_SAMPLE_SECTION_ENROLLMENT_STUDENT = deepcopy(SAMPLE_STUDENT_1)
POWERSCHOOL_API_SAMPLE_SECTION_ENROLLMENT_STUDENT["student"]["id"] = \
    POWERSCHOOL_API_SAMPLE_SECTION_ENROLLMENT["section_enrollment"]
POWERSCHOOL_API_SAMPLE_SECTION_ENROLLMENT_STUDENT["student"]["school_enrollment"]["school_id"] = 3

POWERSCHOOL_API_STAFF_TEACHER_1 = json.loads("""
{
  "staff": {
    "@expansions": "addresses, emails, phones, school_affiliations",
    "@extensions": "s_az_ssf_x,s_ssf_ncea_x",
    "id": 65,
    "local_id": 5,
    "name": {
        "first_name": "Pav",
        "last_name": "koyilada"
    },
    "addresses": "",
    "emails": {
      "work_email": "pkoyilada@strongmind.com"
    },
    "phones": {
      "home_phone": 1234567890
    },
    "school_affiliations": {
        "school_affiliation": {
            "school_id": 3,
            "type": 1,
            "status": 1
        }
    },
    "users_dcid": 63
  }
}
""")

POWERSCHOOL_API_STAFF_TEACHER_2 = json.loads("""
{
  "staff": {
    "@expansions": "addresses, emails, phones, school_affiliations",
    "@extensions": "s_az_ssf_x,s_ssf_ncea_x",
    "id": 67,
    "local_id": "Jeremy.Johnson",
    "admin_username": "Jeremy.Johnson",
    "teacher_username": "johnny_teach",
    "name": {
      "first_name": "Jeremy",
      "middle_name": "Middle",
      "last_name": "Johnson"
    },
    "addresses": {
      "home": {
        "street": "123 Main St",
        "city": "Phoenix",
        "state_province": "AZ",
        "postal_code": 85250
      }
    },
    "emails": {
      "work_email": "Jeremy.Johnson@strongmind.com"
    },
    "phones": {
      "home_phone": 1234567890
    },
    "school_affiliations": {
      "school_affiliation": [
        {
          "school_id": 0,
          "type": 2,
          "status": 1
        },
        {
          "school_id": 3,
          "type": 1,
          "status": 1
       }
     ]
    },
    "users_dcid": 64
  }
}
""")

POWERSCHOOL_API_STAFF_TEACHER_MINIMAL = json.loads("""
{
   "staff": {
      "@expansions": "addresses, emails, phones, school_affiliations",
      "@extensions": "s_az_ssf_x,s_ssf_ncea_x",
      "id": 111,
      "local_id": 987654321,
      "name": {
         "first_name": "Basic",
         "last_name": "Minimal"
      },
      "addresses": "",
      "emails": "",
      "phones": "",
      "school_affiliations": {
         "school_affiliation": {
            "school_id": 0,
            "type": 0,
            "status": 1
         }
      },
      "users_dcid": 110
   }
}
""")

class PowerSchoolStaffTeacherAPIItemFactory(factory.DictFactory):
    """The resulting JSON from hitting PowerSchool's API at /ws/v1/staff"""

    id = factory.Faker('random_int')
    local_id = factory.Faker('random_int')
    name = factory.SubFactory(factory.DictFactory, first_name=factory.Faker('first_name'),
                              last_name=factory.Faker('last_name'))
    addresses = ""
    emails = factory.SubFactory(factory.DictFactory, work_email=factory.Faker('email'))
    users_dcid = factory.Faker('random_int')
    school_affiliations = factory.Dict({
        "school_affiliation": {
            "school_id": 3,
            "type": 1,
            "status": 1
        }
    })

    @factory.lazy_attribute
    def phones(self):
        return {
            "home_phone": factory.Faker('random_number', digits=10).generate()
        }


class PowerSchoolStaffTeacherAPIFactory(factory.DictFactory):
    staff = factory.SubFactory(PowerSchoolStaffTeacherAPIItemFactory)


class PowerSchoolStaffTeacherAPIWithMultipleSchoolsFactory(PowerSchoolStaffTeacherAPIItemFactory):
    """A PowerSchoolStaffTeacherAPIFactory, but where school_affiliations has multiple schools inside rather than
    just 1 """

    @factory.lazy_attribute
    def school_affiliations(self):
        return {
            "school_affiliation": [
                {
                    "school_id": 0,  # seems like school ID 0 is the district office
                    "type": 2,  # type 2 for staff is "Staff" type
                    "status": 1  # 1 is enabled
                },
                {
                    "school_id": 3,
                    # school ID is the DCID for a school, and commonly the first school added by humans starts at 3.
                    # (I think 2 is the graduation school, aka school number 999999)
                    "type": 1,  # type 1 is for is "Teacher" type
                    "status": 1
                },
                {  # a random school this teacher is part of
                    "school_id": factory.Faker('random_int').generate(),
                    "type": 1,
                    "status": 1
                },
                {  # a random school this teacher was part of, but is no longer -- disabled/status != 1
                    "school_id": factory.Faker('random_int').generate(),
                    "type": 1,
                    "status": 0
                },
                {  # a random school this teacher was part of, but is no longer -- disabled/status=2 (per PowerSchool API docs)
                    "school_id": factory.Faker('random_int').generate(),
                    "type": 1,
                    "status": 2
                },
            ]
        }

class PowerTeacherPro_TeacherCategory(factory.DictFactory):
   # "$breach_mitigation": "RxVglrCDCdLsVEWed", # XXX: What is this? It's randomzed and returned by PowerSchool's API but we don't use it at all
   _categoryschoolexcludeassociations = factory.List([])
   _id = factory.SelfAttribute('teachercategoryid')
   _name = "teachercategory"
   _teachercategorysectionexcludeassociations = factory.List([])
   categorytype = factory.Faker('random_elements', elements=['district', 'user'])
   color = factory.Faker('numerify', text='%') # Generate a string of just one digit 1-9, e.g. '1' or '4', etc
   defaultpublishoption = "Immediately"
   defaulttotalvalue = 0.0
   displayposition = factory.Faker('random_int')
   districtteachercategoryid = 1
   isactive = factory.Faker('boolean')
   isdefaultpublishscores = factory.Faker('boolean')
   isinfinalgrades = factory.Faker('boolean')
   isusermodifiable = factory.Faker('boolean')
   name = factory.Faker('sentence')
   teachercategoryid = factory.Faker('random_int')
   teachermodified = factory.Faker('boolean')
   usersdcid = factory.Faker('random_int')

class PowerTeacherPro_SectionAssignment(factory.DictFactory):
   _assignmentstandardassociations = factory.List([])
   createdbyplugin = factory.Faker('numerify', text='%##')
   _name = "assignment"
   _assignmentsections = factory.List([
      factory.Dict({
         "_name": "assignmentsection",
         "minvalues": factory.Dict({
            "minpercent": 0,
            "minpoints": 0,
            "mingrade": "F",
         }),
         "_assignmentstudentassociations": [],
         "description": factory.LazyAttribute(lambda o: f"<p>{factory.Faker('sentence').generate()}</p>\n"),
         "scoreentrypoints": factory.Faker('random_int', min=0, max=100),
         "weight": 1,
         "islocked": factory.Faker('boolean'),
         "isscoringneeded": factory.Faker('boolean'),
         "sectionsdcid": factory.Faker('random_int'),
         "totalpointvalue": factory.LazyAttribute(lambda o: o.scoreentrypoints * o.weight),
         "assignmentsectionid": factory.Faker('random_int'),
         "iscountedinfinalgrade": factory.Faker('boolean'),
         "duedate": factory.Faker('date'),
         "name": factory.Faker('word'),
         "scoretype": "POINTS",
         "_assignmentcategoryassociations": factory.List([
            factory.Dict({
               "assignmentcategoryassocid": factory.Faker('random_int'),
               "_name": "assignmentcategoryassoc",
               "teachercategoryid": factory.Faker('random_int'),
               "_id": factory.SelfAttribute('assignmentcategoryassocid'),
               "isprimary": factory.Faker('boolean'),
            })
         ]),
         "_id": factory.SelfAttribute('assignmentsectionid'),
      })
   ])
   _id = factory.SelfAttribute('assignmentid')
   hasstandards = factory.Faker('boolean')
   assignmentid = factory.Faker('random_int')
   hasextracriteria = factory.Faker('boolean')
