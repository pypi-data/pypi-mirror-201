import base64
import json
import random
import uuid

import pytest
import responses
from faker import Faker

from powerschool_client import PowerSchoolClient
from powerschool_client.errors import PowerSchoolClientError, EntityNotFoundError, PowerSchoolDownError
from powerschool_client.tokens import TokenCredential, TokenManager
from test.factories.contact_access_fixtures import CONTACT_ACCESS_QUERY_RESULT_1
from test.factories.powerschool_api_results import SAMPLE_POWERSCHOOL_INSERT_STUDENT_ERROR, \
    SAMPLE_POWERSCHOOL_INSERT_STUDENT_SINGLE_WARNING, \
    PowerSchoolStaffTeacherAPIFactory
from test.factories.student import SAMPLE_STUDENT_1
from test.response_mocks import add_authenticated_payload, add_powerschool_down_payload

fake = Faker()


class TestPowerSchoolClient:
    def setup(self):
        self.client_id = str(uuid.uuid4())
        self.client_secret = str(uuid.uuid4())
        self.auth_content = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode())
        self.domain = fake.hostname()

        self.responses = responses.RequestsMock()
        self.responses.start()

        self.auth_token = str(uuid.uuid4())

        credentials = {}
        credentials[self.domain] = TokenCredential(
            self.domain, self.client_id, self.client_secret)

        self.responses.add_callback(
            responses.POST,
            f"https://{self.domain}/oauth/access_token/",
            callback=self.picky_oauth_token,
            content_type='application/json',
        )

        self.token_manager = TokenManager(credentials)

        self.target = PowerSchoolClient(self.token_manager)

    def teardown(self):
        self.responses.stop(allow_assert=False)
        self.responses.reset()

    def test_basic(self):
        """There is a PowerSchoolClient class which accepts OAuth Client ID and Secret"""
        self.target

    def picky_oauth_token(self, request):
        if request.headers['Authorization'] != f"Basic {self.auth_content.decode()}":
            return (401, {}, '{"error":"invalid_client"}')
        if request.body != "grant_type=client_credentials":
            return (401, {}, '{"error":"bad_request"}')
        return (200, {}, json.dumps({'access_token': self.auth_token, 'expires_in': str(random.randrange(9999))}))

    def test_fetches_students_from_api(self):
        """A PowerSchoolClient fetches students from the API"""
        student_id = random.randrange(10000)
        add_authenticated_payload(
            self.responses,
            responses.GET,
            f"https://{self.domain}/ws/v1/student/{student_id}?expansions=demographics,addresses,alerts,phones,school_enrollment,ethnicity_race,contact,contact_info,initial_enrollment,schedule_setup,fees,lunch",
            body=json.dumps(SAMPLE_STUDENT_1),
            status=200,
            auth=f"Bearer {self.auth_token}"
        )

        student = self.target.get(
            f"https://{self.domain}/ws/v1/student/{student_id}",
            'STUDENTS'
        )

        assert student == SAMPLE_STUDENT_1
        assert self.responses.calls[1].request.headers["Accept"] == "application/json"

    def test_fetches_sections_from_api(self):
        """A PowerSchoolClient fetches sections from the API"""
        section_id = random.randrange(10000)
        add_authenticated_payload(
            self.responses,
            responses.GET,
            f"https://{self.domain}/ws/v1/section/{section_id}?expansions=term",
            body=json.dumps(SAMPLE_STUDENT_1),
            status=200,
            auth=f"Bearer {self.auth_token}"
        )

        student = self.target.get(
            f"https://{self.domain}/ws/v1/section/{section_id}",
            'SECTIONS'
        )

        assert student == SAMPLE_STUDENT_1
        assert self.responses.calls[1].request.headers["Accept"] == "application/json"

    def test_fetching_staff_from_api(self):
        """When asking a PowerSchoolClient to fetch a staff API resource, it returns the staff member, using expansions
        so that we return all the information available in the powerschool API for a member of staff"""
        assert 'TEACHERS' in self.target.expansions
        staff_id = random.randrange(10000)
        staff_fake = PowerSchoolStaffTeacherAPIFactory(staff__id=staff_id)
        staff_fake_json = json.dumps(staff_fake)
        self.responses.add(
            responses.GET,
            f"https://{self.domain}/ws/v1/staff/{staff_id}?expansions=addresses,emails,phones,school_affiliations",
            body=staff_fake_json,
            status=200,
        )

        staff = self.target.get(
            f"https://{self.domain}/ws/v1/staff/{staff_id}",
            'TEACHERS'
        )

        assert staff == staff_fake

    def test_api_errors_are_raised(self):
        """A PowerSchoolClient will expose errors that happen"""
        student_id = random.randrange(10000)
        url = f"https://{self.domain}/ws/v1/student/{student_id}?expansions=demographics,addresses,alerts,phones,school_enrollment,ethnicity_race,contact,contact_info,initial_enrollment,schedule_setup,fees,lunch"
        self.responses.add(
            responses.GET,
            url,
            body="nope",
            status=403,
        )

        with pytest.raises(PowerSchoolClientError) as exception:
            self.target.get(f"https://{self.domain}/ws/v1/student/{student_id}", 'STUDENTS')

        assert exception.value.response is not None
        assert exception.value.request is not None
        assert exception.value.response.status_code == 403
        assert exception.value.request.url == url

    def test_get_raises_when_powerschool_is_down(self):
        student_id = fake.uuid4()
        url = f"https://{self.domain}/ws/v1/student/{student_id}?expansions=demographics,"\
              f"addresses,alerts,phones,school_enrollment,ethnicity_race,contact,contact_info,"\
              f"initial_enrollment,schedule_setup,fees,lunch"
        add_powerschool_down_payload(self.responses,
                                     responses.GET,
                                     url,
                                     auth=f"Bearer {self.auth_token}")
        with pytest.raises(PowerSchoolDownError) as exception:
            self.target.get(f"https://{self.domain}/ws/v1/student/{student_id}", 'STUDENTS')
        assert exception.value.request.url is not None
        assert exception.value.dependency_name == 'PowerSchool'

    def test_fetches_weird_entity_type(self):
        """A PowerSchoolClient fetches the literal URL with no expansions when passed an unknown entity type"""
        student_id = random.randrange(10000)
        self.responses.add(
            responses.GET,
            f"https://{self.domain}/ws/v1/student/{student_id}",
            body=json.dumps(SAMPLE_STUDENT_1),
            status=200,
        )

        student = self.target.get(
            f"https://{self.domain}/ws/v1/student/{student_id}",
            fake.word()
        )

        assert student == SAMPLE_STUDENT_1

    def test_successful_errors_are_raised(self):
        """When PowerSchool sends us a 200 HTTP code but with status: ERROR,
        make sure we raise an exception"""

        self.responses.add(
            responses.POST,
            f"https://{self.domain}/ws/v1/student/",
            body=json.dumps(SAMPLE_POWERSCHOOL_INSERT_STUDENT_ERROR),
            status=200,
        )

        with pytest.raises(PowerSchoolClientError):
            self.target.post(
                f"https://{self.domain}/ws/v1/student/", {})

    def test_empty_post_body_returns_none(self):
        """When PowerSchool returns an empty response body in response to a POST, return None"""

        self.responses.add(
            responses.POST,
            f"https://{self.domain}/ws/v1/student/",
            body="",
            status=200,
        )

        response = self.target.post(
            f"https://{self.domain}/ws/v1/student/", {})

        assert response == None

    def test_post_raises_when_powerschool_is_down(self):
        add_powerschool_down_payload(self.responses,
                                     responses.POST,
                                     f"https://{self.domain}/ws/v1/student/",
                                     auth=f"Bearer {self.auth_token}")
        with pytest.raises(PowerSchoolDownError) as exception:
            self.target.post(f"https://{self.domain}/ws/v1/student/", {})
        assert exception.value.request.url is not None

    def test_post_raises_custom_error_with_http_info(self):
        # Arrange
        url = f"https://{self.domain}/ws/v1/student/"
        add_authenticated_payload(
            self.responses,
            responses.POST,
            url,
            body="{}",
            status=503,
            auth=f"Bearer {self.auth_token}"
        )

        # Act
        with pytest.raises(PowerSchoolClientError) as exception:
            self.target.post(f"https://{self.domain}/ws/v1/student/", {})

        # Assert
        assert exception.value.response is not None
        assert exception.value.request is not None
        assert exception.value.response.status_code == 503
        assert exception.value.request.url == url

    def test_empty_put_body_returns_none(self):
        """When PowerSchool returns an empty response body in response to a PUT, return None"""

        self.responses.add(
            responses.PUT,
            f"https://{self.domain}/ws/v1/student/",
            body="",
            status=200,
        )

        response = self.target.put(f"https://{self.domain}/ws/v1/student/", {})

        assert response == None

    def test_raises_error_when_entity_not_found(self):
        """When PowerSchool sends us a 404 HTTP code raise an Entity not found error"""
        student_id = random.randrange(10000)
        url = f"https://{self.domain}/ws/v1/student/{student_id}?expansions=demographics,addresses,alerts,phones,school_enrollment,ethnicity_race,contact,contact_info,initial_enrollment,schedule_setup,fees,lunch"
        self.responses.add(
            responses.GET,
            url,
            body="nope",
            status=404,
        )

        with pytest.raises(EntityNotFoundError) as exception:
            self.target.get(f"https://{self.domain}/ws/v1/student/{student_id}", 'STUDENTS')

        assert exception.value.response is not None
        assert exception.value.request is not None
        assert exception.value.response.status_code == 404
        assert exception.value.request.url == url
        assert exception.value.dependency_name == 'PowerSchool'

    def test_successful_single_warning_is_ok(self):
        """
        When PowerSchool sends us a 200 HTTP code but with single status:
        WARNING, thus as an object instead of an array, and we don't raise an
        error
        """

        self.responses.add(
            responses.POST,
            f"https://{self.domain}/ws/v1/student/",
            body=json.dumps(SAMPLE_POWERSCHOOL_INSERT_STUDENT_SINGLE_WARNING),
            status=200,
        )

        try:
            response = self.target.post(
                f"https://{self.domain}/ws/v1/student/", {})
        except PowerSchoolClientError:
            pytest.fail(
                "Unexpected PowerSchoolClientError raised from a warning status")

    def test_successful_power_query(self):
        add_authenticated_payload(
            self.responses,
            responses.POST,
            f"https://{self.domain}/ws/schema/query/com.strongmind.contact_data_access_all_emails",
            body=json.dumps(CONTACT_ACCESS_QUERY_RESULT_1),
            status=200,
            auth=f"Bearer {self.auth_token}"
        )

        result = self.target.power_query(
            f"https://{self.domain}/ws/schema/query/com.strongmind.contact_data_access_all_emails", {})

        assert result == CONTACT_ACCESS_QUERY_RESULT_1

    def test_negative_power_query(self):
        self.responses.add(
            responses.POST,
            f"https://{self.domain}/ws/schema/query/com.strongmind.contact_data_access_all_emails",
            body=json.dumps({"message": "illegal"}),
            status=400,
        )
        with pytest.raises(PowerSchoolClientError):
            self.target.power_query(
                f"https://{self.domain}/ws/schema/query/com.strongmind.contact_data_access_all_emails",
                {"$q": "invalid data"})

    def test_power_query_when_powerschool_is_down(self):
        add_powerschool_down_payload(
            self.responses,
            responses.POST,
            f"https://{self.domain}/ws/schema/query/com.strongmind.contact_data_access_all_emails",
            auth=f"Bearer {self.auth_token}")
        with pytest.raises(PowerSchoolDownError) as exception:
            self.target.power_query(
                f"https://{self.domain}/ws/schema/query/com.strongmind.contact_data_access_all_emails", {})
        assert exception.value.request.url is not None

    def test_empty_power_query(self):
        """An empty power query has a record array added so that downstream clients don't need to check for presence"""
        add_authenticated_payload(
            self.responses,
            responses.POST,
            f"https://{self.domain}/ws/schema/query/com.strongmind.contact_data_access_all_emails",
            body=json.dumps({"@extensions": ""}),
            status=200,
            auth=f"Bearer {self.auth_token}"
        )

        result = self.target.power_query(
            f"https://{self.domain}/ws/schema/query/com.strongmind.contact_data_access_all_emails", {})

        assert "record" in result
        assert result["record"] == []

    def test_successful_post_call(self):
        add_authenticated_payload(
            self.responses,
            responses.POST,
            f"https://{self.domain}/ws/v1/student",
            body="{}",
            status=200,
            auth=f"Bearer {self.auth_token}"
        )

        self.target.post(f"https://{self.domain}/ws/v1/student", {})

    def test_successful_put_call(self):
        add_authenticated_payload(
            self.responses,
            responses.PUT,
            f"https://{self.domain}/ws/v1/event_subscription",
            body=json.dumps(CONTACT_ACCESS_QUERY_RESULT_1),
            status=200,
            auth=f"Bearer {self.auth_token}"
        )

        self.target.put(f"https://{self.domain}/ws/v1/event_subscription", {})

    def test_put_raises_when_powerschool_is_down(self):
        add_powerschool_down_payload(self.responses,
                                     responses.PUT,
                                     f"https://{self.domain}/ws/v1/event_subscription",
                                     auth=f"Bearer {self.auth_token}")
        with pytest.raises(PowerSchoolDownError) as exception:
            self.target.put(f"https://{self.domain}/ws/v1/event_subscription", {})
        assert exception.value.request.url is not None

    def test_negative_put_call(self):
        self.responses.add(
            responses.PUT,
            f"https://{self.domain}/ws/v1/event_subscription",
            status=500,
        )

        with pytest.raises(PowerSchoolClientError):
            self.target.put(
                f"https://{self.domain}/ws/v1/event_subscription", {})

    def test_fetching_staff_from_api_with_no_expansions(self):
        """When asking a PowerSchoolClient with no expansions to fetch a staff API resource, 
        it returns the staff member, not using expansions
        so that we return only the information we need in the powerschool API for a member of staff"""
        client = PowerSchoolClient(self.token_manager, {})
        assert 'TEACHERS' not in client.expansions
        staff_id = random.randrange(10000)
        staff_fake = PowerSchoolStaffTeacherAPIFactory(staff__id=staff_id)
        staff_fake_json = json.dumps(staff_fake)
        self.responses.add(
            responses.GET,
            f"https://{self.domain}/ws/v1/staff/{staff_id}",
            body=staff_fake_json,
            status=200,
        )

        staff = client.get(
            f"https://{self.domain}/ws/v1/staff/{staff_id}",
            'TEACHERS'
        )

        assert staff == staff_fake

    def test_fetching_staff_from_api_with_limited_expansions(self):
        """When asking a PowerSchoolClient with limited expansions to fetch a staff API resource, 
        it returns the staff member, with only emails expansion
        so that we return only the information we need in the powerschool API for a member of staff"""
        client = PowerSchoolClient(self.token_manager, {"TEACHERS": ["emails"]})
        assert 'TEACHERS' in client.expansions
        staff_id = random.randrange(10000)
        staff_fake = PowerSchoolStaffTeacherAPIFactory(staff__id=staff_id)
        staff_fake_json = json.dumps(staff_fake)
        self.responses.add(
            responses.GET,
            f"https://{self.domain}/ws/v1/staff/{staff_id}?expansions=emails",
            body=staff_fake_json,
            status=200,
        )

        staff = client.get(
            f"https://{self.domain}/ws/v1/staff/{staff_id}",
            'TEACHERS'
        )

        assert staff == staff_fake

    def test_successful_delete_call(self):
        add_authenticated_payload(
            self.responses,
            responses.DELETE,
            f"https://{self.domain}/ws/schema/table/U_SM_UUID/123",
            body=None,
            status=204,
            auth=f"Bearer {self.auth_token}"
        )

        self.target.delete(f"https://{self.domain}/ws/schema/table/U_SM_UUID/123")

    def test_delete_raises_when_powerschool_is_down(self):
        add_powerschool_down_payload(self.responses,
                                     responses.DELETE,
                                     f"https://{self.domain}/ws/schema/table/U_SM_UUID/123",
                                     auth=f"Bearer {self.auth_token}")
        with pytest.raises(PowerSchoolDownError) as exception:
            self.target.delete(f"https://{self.domain}/ws/schema/table/U_SM_UUID/123")
        assert exception.value.request.url is not None

    def test_non_existent_delete_call(self):
        """If delete results in a 404, swallow the error because we don't care"""
        add_authenticated_payload(
            self.responses,
            responses.DELETE,
            f"https://{self.domain}/ws/schema/table/U_SM_UUID/123",
            body=None,
            status=404,
            auth=f"Bearer {self.auth_token}"
        )

        self.target.delete(f"https://{self.domain}/ws/schema/table/U_SM_UUID/123")

    def test_negative_delete_call(self):
        url = f"https://{self.domain}/ws/schema/table/U_SM_UUID/123"
        self.responses.add(
            responses.DELETE,
            url,
            status=500,
        )

        with pytest.raises(PowerSchoolClientError) as exception:
            self.target.delete(f"https://{self.domain}/ws/schema/table/U_SM_UUID/123")

        assert exception.value.response is not None
        assert exception.value.request is not None
        assert exception.value.response.status_code == 500
        assert exception.value.request.url == url

    def test_get_raises_when_powerschool_is_down_and_powerschool_changes_their_url(self):
        student_id = fake.uuid4()
        add_powerschool_down_payload(self.responses,
                                     responses.GET,
                                     f"https://{self.domain}/ws/v1/student/{student_id}?expansions=demographics,"
                                     f"addresses,alerts,phones,school_enrollment,ethnicity_race,contact,contact_info,"
                                     f"initial_enrollment,schedule_setup,fees,lunch",
                                     auth=f"Bearer {self.auth_token}",
                                     redirect_url="https://powerschool-got-down.com/")
        with pytest.raises(PowerSchoolDownError) as exception:
            self.target.get(f"https://{self.domain}/ws/v1/student/{student_id}", 'STUDENTS')
        assert exception.value.request.url is not None
