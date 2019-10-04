from shared.seed_data.request_data import create_request_data
from shared.seed_data.make_requests import make_request
from shared.seed_data.seed_data_classes.seed_good import SeedGood
from shared.seed_data.seed_data_classes.seed_user import SeedUser
from shared.seed_data.seed_data_classes.seed_organisation import SeedOrganisation
from shared.seed_data.seed_data_classes.seed_clc import SeedClc
from shared.seed_data.seed_data_classes.seed_party import SeedParty
from shared.seed_data.seed_data_classes.seed_ecju import SeedEcju
from shared.seed_data.seed_data_classes.seed_picklist import SeedPicklist
from shared.seed_data.seed_data_classes.seed_case import SeedCase
from shared.seed_data.seed_data_classes.seed_queue import SeedQueue
from shared.seed_data.seed_data_classes.seed_additional_document import SeedAdditionalDocument
from shared.seed_data.check_documents import check_documents


class SeedData:
    base_url = ''
    gov_headers = {'content-type': 'application/json'}
    export_headers = {'content-type': 'application/json'}
    context = {}
    logging = True
    org_name = "Test Org"

    def __init__(self, seed_data_config):
        exporter_user = seed_data_config['exporter']
        gov_user = seed_data_config['gov']
        test_s3_key = seed_data_config['s3_key']
        self.base_url = seed_data_config['api_url'].rstrip('/')
        self.request_data = create_request_data(
            exporter_user=exporter_user,
            test_s3_key=test_s3_key,
            gov_user=gov_user
        )
        self.seed_user = SeedUser(self.base_url, self.gov_headers, self.export_headers, self.request_data, self.context)
        self.seed_user.auth_gov_user()
        self.seed_org = SeedOrganisation(self.base_url, self.gov_headers, self.export_headers, self.request_data,
                                         self.context)
        self.seed_org.setup_org()
        self.seed_user.auth_export_user()

        self.seed_good = SeedGood(self.base_url, self.gov_headers, self.export_headers, self.request_data, self.context)
        self.seed_good.add_good()

        self.seed_clc = SeedClc(self.base_url, self.gov_headers, self.export_headers, self.request_data, self.context)
        self.seed_party = SeedParty(self.base_url, self.gov_headers, self.export_headers, self.request_data, self.context)
        self.seed_ecju = SeedEcju(self.base_url, self.gov_headers, self.export_headers, self.request_data, self.context)
        self.seed_picklist = SeedPicklist(self.base_url, self.gov_headers, self.export_headers, self.request_data, self.context)
        self.seed_case = SeedCase(self.base_url, self.gov_headers, self.export_headers, self.request_data, self.context)
        self.seed_queue = SeedQueue(self.base_url, self.gov_headers, self.export_headers, self.request_data, self.context)
        self.seed_additional_doc = SeedAdditionalDocument(self.base_url, self.gov_headers, self.export_headers, self.request_data, self.context)

    def log(self, text):
        print(text)

    def add_to_context(self, name, value):
        self.log(name + ': ' + str(value))
        self.context[name] = value

    def add_site(self, draft_id):
        self.log("Adding site: ...")
        make_request("POST", base_url=self.base_url, url='/drafts/' + draft_id + '/sites/', headers=self.export_headers,
                     body={'sites': [self.context['primary_site_id']]})

    def create_draft(self):
        self.log("Creating draft: ...")
        data = self.request_data['draft'] if draft is None else draft
        response = make_request("POST", base_url=self.base_url, url='/drafts/', headers=self.export_headers, body=data)
        return response.json()['draft']['id']

    def add_draft(self, draft=None, good=None, enduser=None, ultimate_end_user=None, consignee=None, third_party=None,
                  additional_documents=None):
        draft_id = self.create_draft()
        self.add_to_context('draft_id', draft_id)
        self.add_site(draft_id)
        self.seed_party.add_end_user(draft_id, enduser)
        self.seed_good.add_good_to_draft(draft_id, good)
        ultimate_end_user_id = self.seed_party.add_ultimate_end_user(draft_id, ultimate_end_user)
        self.seed_party.add_consignee(draft_id, consignee)
        third_party_id = self.seed_party.add_third_party(draft_id, third_party)
        additional_document_id = self.seed_additional_doc.add_additional_document(draft_id, additional_documents)
        check_documents(base_url=self.base_url, export_headers=self.export_headers, draft_id=draft_id,
                        ultimate_end_user_id=ultimate_end_user_id, third_party_id=third_party_id,
                        additional_document_id=additional_document_id)

    def add_open_draft(self, draft=None):
        self.log("Creating draft: ...")
        data = self.request_data['draft'] if draft is None else draft
        response = make_request("POST", base_url=self.base_url, url='/drafts/', headers=self.export_headers, body=data)
        draft_id = response.json()['draft']['id']
        self.add_to_context('draft_id', draft_id)
        self.log("Adding site: ...")
        make_request("POST", base_url=self.base_url, url='/drafts/' + draft_id + '/sites/', headers=self.export_headers,
                          body={'sites': [self.context['primary_site_id']]})
        self.log("Adding countries: ...")
        make_request("POST", base_url=self.base_url, url='/drafts/' + draft_id + '/countries/', headers=self.export_headers,
                          body={'countries': ['US', 'AL', 'ZM']})
        self.log("Adding goods_type: ...")
        data = {
            'description': 'A goods type',
            'is_good_controlled': True,
            'control_code': 'ML1a',
            'is_good_end_product': True,
            'content_type': 'draft',
            'object_id': draft_id
        }
        make_request("POST", base_url=self.base_url, url='/goodstype/', headers=self.export_headers, body=data)

    def submit_application(self, draft_id=None):
        self.log('submitting application: ...')
        draft_id_to_submit = draft_id if None else self.context['draft_id']  # noqa
        data = {'id': draft_id_to_submit}
        response = make_request('POST', base_url=self.base_url, url='/applications/', headers=self.export_headers, body=data)
        item = response.json()['application']
        self.add_to_context('application_id', item['id'])
        self.add_to_context('case_id', item['case_id'])

    def submit_open_application(self, draft_id=None):
        self.log("submitting application: ...")
        draft_id_to_submit = draft_id if None else self.context['draft_id']  # noqa
        data = {'id': draft_id_to_submit}
        response = make_request("POST", base_url=self.base_url, url='/applications/', headers=self.export_headers, body=data)
        item = response.json()['application']
        self.add_to_context('open_application_id', item['id'])
        self.add_to_context('open_case_id', item['case_id'])
