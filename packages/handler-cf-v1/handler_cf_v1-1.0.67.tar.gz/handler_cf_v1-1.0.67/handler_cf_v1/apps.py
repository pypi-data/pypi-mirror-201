from typing import Any
import requests
import json
from .exceptions import ApiError
from five9 import Five9
from ast import literal_eval
from sqlalchemy import create_engine
from google.cloud import bigquery


class BigQuery:

    def __init__(self) -> None:
        self.bq_client = self.set_bq_client()

    def set_bq_client(self):
        return bigquery.Client()

    def insert_row(self, table_id, row):
        errors = self.bq_client.insert_rows_json(table_id, row)
        if errors != []:
            raise Exception(f"Something went wrong: {errors}")
        return "OK"

    def get_table_columns(self, table_id):
        return self.bq_client.get_table(table_id).schema


class SierraInteractive:

    def __init__(self, api_key: str, originating_system: str) -> None:
        self.api_key = api_key
        self.find_leads_ep = "https://api.sierrainteractivedev.com/leads/find?{}"
        self.add_note_ep = "https://api.sierrainteractivedev.com/leads/{}/note"
        self.retrieve_lead_details_ep = "https://api.sierrainteractivedev.com/leads/get/{}"
        self.add_new_lead_ep = "https://api.sierrainteractivedev.com/leads"
        self.headers = {
            "Content-Type": "application/json",
            "Sierra-ApiKey": self.api_key,
            "Sierra-OriginatingSystemName": originating_system
        }

    def find_leads(self, lead_phone: str, lead_email: str) -> Any:
        """
        Returns the lead object of the first record in the array returned by Sierra API.
        :param str lead_phone: the phone number of the lead to search for, i.e. +13233455555.
        :param str lead_email: the email of the lead to search for.
        :return None if no lead is found or the lead data (dict) if at least one is found.
        :raises ApiError when response status code is not equal to 200.
        """

        if not lead_email:
            response = requests.get(
                self.find_leads_ep.format(f'phone={lead_phone.strip()}'),
                headers=self.headers
            )
            if response.status_code != 200:
                raise ApiError(response.status_code)
            json_response = response.json()
            if json_response['data']['totalRecords'] > 0:
                return json_response['data']['leads'][0]
            return None
        response = requests.get(
            self.retrieve_lead_details_ep.format(lead_email.strip()),
            headers=self.headers
        )
        if response.json()['success'] == True:
            return response.json()['data']
        return None

    def add_new_lead(self, payload: dict):
        """
        Returns the lead object of the record created in Sierra API.
        :param dict payload: the data to POST to the Add New Lead EP using the specifications required by Sierra
        https://api.sierrainteractivedev.com/#leads-create
        Example payload:
        {
            "firstName": "John",
            "lastName": "Doe",
            "email": "johndoe@server.com",
            "password": "123456",
            "emailStatus": "TwoWayEmailing",
            "phone": "(123) 456-7890",
            "phoneStatus": "TalkingToProspect",
            "birthDate": "2000-01-21",
            "referralFee": true,
            "sendRegistrationEmail": true,
            "note": "Some note",
            "leadType": 1,
            "source": "Lead source",
            "shortSummary": "Just looking",
            "tags": [ "Tag_1", "Tag_2"],
            "partnerLink": "https://partern-site.com/lead-page/123",
            "assignTo": {
                "agentSiteId": 123456,
                "agentUserId": 234567,
                "agentUserEmail": "agent@site.com"
            }
        }
        :return the lead object (dict) of the record created in Sierra API.
        :raise ApiError when lead creation is not successful.
        """
        if not payload['email']:
            raise Exception("Email is required for creating leads")
        response = requests.post(
            url=self.add_new_lead_ep,
            headers=self.headers,
            data=json.dumps(payload)
        )
        if response.status_code != 200:
            raise ApiError(response.status_code)
        return response.json()['data']

    def add_note(self, lead_id: str, notes: str) -> Any:
        """
        Add note  to lead in Sierra.
        :param str lead_id: the ID of the lead to update.
        :param str notes: the The notes to add to the lead.
        :return dict with success response
        :raises ApiError when response status code is not equal to 200.
        """
        message = {
            "message": notes
        }
        response = requests.post(
            url=self.add_note_ep.format(lead_id),
            headers=self.headers,
            data=json.dumps(message)
        )
        if response.status_code != 200:
            raise ApiError(response.status_code)
        return response.json()


class Five9Custom(Five9):

    def __init__(self, username, password):
        super().__init__(username, password)

    def search_contacts(self, criteria):
        response = self.configuration.getContactRecords(
            lookupCriteria=criteria)
        return literal_eval(str(response))

    def get_campaign_profile(self, profile_name):
        response = self.configuration.getCampaignProfiles(
            namePattern=profile_name)
        return literal_eval(str(response[0]))

    def update_campaign_profile(self, profile_confing):
        return self.configuration.modifyCampaignProfile(profile_confing)

    def get_inbound_campaigns(self, name_pattern=None):
        response = self.configuration.getCampaigns(
            campaignNamePattern=".*" if name_pattern is None else name_pattern, campaignType="INBOUND")
        return literal_eval(str(response))

    def get_outbound_campaigns(self, name_pattern=None):
        response = self.configuration.getCampaigns(
            campaignNamePattern=".*" if name_pattern is None else name_pattern, campaignType="OUTBOUND"
        )
        return literal_eval(str(response))

    def get_campaign_dnis_list(self, campaign_name):
        return self.configuration.getCampaignDNISList(campaignName=campaign_name)

    def update_dnis_list(self, campaign_name: str, dnis_list: list):
        return self.configuration.addDNISToCampaign(
            campaignName=campaign_name,
            DNISList=dnis_list
        )

    def remove_dnis_list(self, campaign_name: str, dnis_list: list):
        return self.configuration.removeDNISFromCampaign(
            campaignName=campaign_name,
            DNISList=dnis_list
        )

    def add_to_dnc(self, numbers: list):
        return self.configuration.addNumbersToDnc(numbers)

    def remove_from_dnc(self, numbers: list):
        return self.configuration.removeNumbersFromDnc(numbers)


class KvCore:

    def __init__(self, api_token) -> None:
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        self.get_contacts_list_ep = "https://api.kvcore.com/v2/public/contacts?filter[{}]={}"
        self.add_note_ep = "https://api.kvcore.com/v2/public/contact/{}/action/note"

    def get_contact(self, email):
        if not email:
            return None
        response = requests.get(
            url=self.get_contacts_list_ep.format("email", email),
            headers=self.headers
        )
        if response.status_code != 200:
            raise ApiError(
                response.status_code
            )
        json_data = response.json()
        if json_data['total'] > 0:
            return json_data['data'][0]
        return None

    def update_notes(self, contact_id, title, notes):
        payload = json.dumps({
            "title": title,
            "details": notes
        })
        response = requests.put(
            url=self.add_note_ep.format(contact_id),
            headers=self.headers,
            data=payload
        )
        if response.status_code == 200:
            return response.json()
        raise ApiError(response.status_code)


class SQLDB:

    def __init__(self, db_credentials) -> None:
        self.db_credentials = db_credentials
        self.conn_string = self.generate_conn_string(
            user=self.db_credentials['user'],
            password=self.db_credentials['password'],
            host=self.db_credentials['host'],
            schema=self.db_credentials['schema'],
            conn_string=self.db_credentials['conn_string'],
        )
        self.engine = create_engine(self.conn_string)

    def execute_sql(self, query_string, multiparams=None):
        if self.engine is None:
            raise ApiError(500)
        with self.engine.connect() as conn:
            if multiparams is None:
                return conn.execute(query_string)
            return conn.execute(query_string, multiparams)

    def generate_conn_string(self, **kwargs):
        user = kwargs.get('user')
        password = kwargs.get('password')
        host = kwargs.get('host')
        schema = kwargs.get('schema')
        conn_string = kwargs.get('conn_string')
        return conn_string.format(user, password, host, schema)


class GHL:

    def __init__(self, agency_api_key, location_id) -> None:
        self.agency_api_key = agency_api_key
        self.location_id = location_id
        self.location_api_key = None
        self.get_location_ep = f'https://rest.gohighlevel.com/v1/locations/{self.location_id}'
        self.contact_ep = 'https://rest.gohighlevel.com/v1/contacts/{}'
        self.contact_lookup_ep = 'https://rest.gohighlevel.com/v1/contacts/lookup?'
        self.custom_fields_ep = "https://rest.gohighlevel.com/v1/custom-fields/"
        self.notes_ep = "https://rest.gohighlevel.com/v1/contacts/{}/notes/"
        self.pipelines_ep = "https://rest.gohighlevel.com/v1/pipelines/"
        self.opportunities_ep = "https://rest.gohighlevel.com/v1/pipelines/{}/opportunities"

    def get_location(self):
        headers = {
            'Authorization': f'Bearer {self.agency_api_key}'
        }
        request = requests.get(url=self.get_location_ep,
                               headers=headers)
        if request.status_code == 200:
            return request.json()
        raise ApiError(request.status_code, list(request.json().values())[
                       0]["message"] + " status code: {}")

    def get_custom_fields(self):
        custom_fields_data = []
        self.location_api_key = self.get_location(
        )['apiKey'] if self.location_api_key is None else self.location_api_key
        headers = {
            'Authorization': f'Bearer {self.location_api_key}'
        }
        response = requests.get(url=self.custom_fields_ep, headers=headers)
        if response.status_code != 200:
            raise ApiError(response.status_code)
        if 'customFields' in response.json():
            custom_fields_data = response.json()
        if len(custom_fields_data) == 0:
            return None
        return custom_fields_data['customFields']

    def contact_lookup(self, query_params):
        contact_data = []
        self.location_api_key = self.get_location(
        )['apiKey'] if self.location_api_key is None else self.location_api_key
        headers = {
            'Authorization': f'Bearer {self.location_api_key}'
        }
        url = self.contact_lookup_ep + query_params
        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            if response.status_code == 422:
                return None
            raise ApiError(response.status_code)
        if 'contacts' in response.json():
            contact_data = response.json()['contacts']
        if len(contact_data) == 0:
            return None
        return contact_data[0]

    def update_contact(self, contact_id, data):
        contact_data = []
        self.location_api_key = self.get_location(
        )['apiKey'] if self.location_api_key is None else self.location_api_key
        headers = {
            'Authorization': f'Bearer {self.location_api_key}',
            'Content-Type': 'application/json'
        }
        url = self.contact_ep.format(contact_id)
        payload = json.dumps(data)
        response = requests.put(url=url, headers=headers, data=payload)
        if response.status_code != 200:
            raise ApiError(response.status_code)
        contact_data = response.json()
        return contact_data

    def add_notes(self, contact_id, notes, user_id):
        notes_data = []
        self.location_api_key = self.get_location(
        )['apiKey'] if self.location_api_key is None else self.location_api_key
        headers = {
            'Authorization': f'Bearer {self.location_api_key}',
            'Content-Type': 'application/json'
        }
        url = self.notes_ep.format(contact_id)
        payload = json.dumps({
            "body": notes,
            "userID": user_id
        })
        response = requests.post(url=url, headers=headers, data=payload)
        if response.status_code != 200:
            raise ApiError(response.status_code)
        notes_data = response.json()
        return notes_data

    def get_pipelines(self):
        pipelines_data = []
        self.location_api_key = self.get_location(
        )['apiKey'] if self.location_api_key is None else self.location_api_key
        headers = {'Authorization': f'Bearer {self.location_api_key}'}
        url = self.pipelines_ep
        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            raise ApiError(response.status_code)
        if 'pipelines' in response.json():
            pipelines_data = response.json()['pipelines']
        if len(pipelines_data) == 0:
            return None
        return pipelines_data

    def get_opportunities(self, pipeline_id, query_params=None):
        opportunities_data = []
        self.location_api_key = self.get_location(
        )['apiKey'] if self.location_api_key is None else self.location_api_key
        headers = {'Authorization': f'Bearer {self.location_api_key}'}
        url = self.opportunities_ep.format(
            pipeline_id) + '?query=' + query_params if query_params else self.opportunities_ep.format(pipeline_id)
        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            raise ApiError(response.status_code)
        if 'opportunities' in response.json():
            opportunities_data = response.json()['opportunities']
        if len(opportunities_data) == 0:
            return None
        return opportunities_data

    def create_opportunity(self, pipeline_id, data):
        opportunity_data = []
        self.location_api_key = self.get_location(
        )['apiKey'] if self.location_api_key is None else self.location_api_key
        headers = {
            'Authorization': f'Bearer {self.location_api_key}',
            'Content-Type': 'application/json'
        }
        url = self.opportunities_ep.format(pipeline_id) + '/'
        payload = json.dumps(data)
        response = requests.post(url=url, headers=headers, data=payload)
        if response.status_code != 200:
            raise ApiError(response.status_code)
        opportunity_data = response.json()
        return opportunity_data

    def update_opportunity(self, pipeline_id, opportunity_id, data):
        opportunity_data = []
        self.location_api_key = self.get_location(
        )['apiKey'] if self.location_api_key is None else self.location_api_key
        headers = {
            'Authorization': f'Bearer {self.location_api_key}',
            'Content-Type': 'application/json'
        }
        url = self.opportunities_ep.format(
            pipeline_id) + '/' + str(opportunity_id)
        payload = json.dumps(data)
        response = requests.put(url=url, headers=headers, data=payload)
        if response.status_code != 200:
            raise ApiError(response.status_code)
        opportunity_data = response.json()
        return opportunity_data
