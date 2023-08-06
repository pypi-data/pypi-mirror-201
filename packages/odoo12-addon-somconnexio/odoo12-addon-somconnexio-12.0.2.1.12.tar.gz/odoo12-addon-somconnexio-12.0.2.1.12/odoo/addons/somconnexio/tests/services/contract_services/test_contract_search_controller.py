import json
import odoo
from faker import Faker
from ...common_service import BaseEMCRestCaseAdmin
from ....services.contract_contract_service import ContractService
from ...helpers import crm_lead_create


class TestContractSearchController(BaseEMCRestCaseAdmin):

    def setUp(self):
        super().setUp()
        self.url = "/api/contract"
        self.partner = self.browse_ref('somconnexio.res_partner_2_demo')
        self.phone_number = "654321123"
        mbl_contract_service_info = self.env[
            'mobile.service.contract.info'
        ].create({
            'phone_number': self.phone_number,
            'icc': '123',
        })
        fake = Faker('es-ES')
        crm_lead = crm_lead_create(self.env, self.partner, "fiber",
                                   portability=True)
        self.mandate = self.env['account.banking.mandate'].create({
            'partner_bank_id': self.partner.bank_ids[0].id,
            'state': 'valid',
            'partner_id': self.partner.id,
            'signature_date': fake.date_time_this_month()
        })
        self.contract = self.env['contract.contract'].create({
            'name': 'Test Contract Mobile',
            'partner_id': self.partner.id,
            'service_partner_id': self.partner.id,
            'invoice_partner_id': self.partner.id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_mobile"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_masmovil"
            ),
            'mobile_contract_service_info_id': mbl_contract_service_info.id,
            'contract_line_ids': [(0, False, {
                'name': 'Mobile',
                'product_id': self.ref('somconnexio.150Min1GB')  # noqa
            })],
            'mandate_id': self.mandate.id,
            'crm_lead_line_id': crm_lead.lead_line_ids[0].id,
            'fiber_signal_type_id': self.ref(
                "somconnexio.FTTH_fiber_signal"
            ),
        })

    @odoo.tools.mute_logger("odoo.addons.auth_api_key.models.ir_http")
    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_without_auth(self):
        response = self.http_get_without_auth()

        self.assertEquals(response.status_code, 403)
        self.assertEquals(response.reason, "FORBIDDEN")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_unknown_parameter(self):
        url = "{}?{}={}".format(self.url, "unknown_parameter", "2828")
        response = self.http_get(url)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.reason, "BAD REQUEST")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_multiple_parameters(self):
        url = "{}?{}={}&{}={}".format(self.url, "code", "111111",
                                      "partner_vat", "ES1828028")
        response = self.http_get(url)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.reason, "BAD REQUEST")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_code_not_found(self):
        url = "{}?{}={}".format(self.url, "code", "111111")
        response = self.http_get(url)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.reason, "NOT FOUND")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_partner_vat_not_found(self):
        url = "{}?{}={}".format(self.url, "partner_vat", "111111")
        response = self.http_get(url)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.reason, "NOT FOUND")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_phone_number_not_found(self):
        url = "{}?{}={}".format(self.url, "phone_number", "111111")
        response = self.http_get(url)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.reason, "NOT FOUND")

    def test_route_contract_search_code_ok(self):
        url = "{}?{}={}".format(self.url, "code", self.contract.code)
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(result[0]["id"], self.contract.id)

    def test_route_contract_search_phone_number_ok(self, *args):
        url = "{}?{}={}".format(self.url, "phone_number", self.contract.phone_number)
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(len(result), 1)
        self.assertEquals(result[0]["id"], self.contract.id)

    def test_route_contract_search_partner_vat_multiple_ok(self, *args):
        another_phone = "77782825"
        new_mbl_contract_service_info = self.env[
            'mobile.service.contract.info'
        ].create({
            'phone_number': another_phone,
            'icc': '1543'
        })
        new_contract = self.env['contract.contract'].create({
            'name': 'Test 2 Contract Mobile',
            'partner_id': self.partner.id,
            'service_partner_id': self.partner.id,
            'invoice_partner_id': self.partner.id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_mobile"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_masmovil"
            ),
            'mobile_contract_service_info_id': new_mbl_contract_service_info.id,
            'mandate_id': self.mandate.id,
        })

        url = "{}?{}={}".format(self.url, "partner_vat", self.partner.vat)
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(len(result), 2)
        self.assertEquals(result[0]["id"], self.contract.id)
        self.assertEquals(result[1]["id"], new_contract.id)

    def test_route_contract_search_to_dict(self):
        result = ContractService(self.env)._to_dict(self.contract)

        self.assertEquals(result["id"], self.contract.id)
        self.assertEquals(result["code"], self.contract.code)
        self.assertEquals(result["customer_firstname"],
                          self.contract.partner_id.firstname)
        self.assertEquals(result["customer_lastname"],
                          self.contract.partner_id.lastname)
        self.assertEquals(result["customer_ref"], self.contract.partner_id.ref)
        self.assertEquals(result["customer_vat"], self.contract.partner_id.vat)
        self.assertEquals(result["phone_number"], self.contract.phone_number)
        self.assertEquals(
            result["current_tariff_product"],
            "SE_SC_REC_MOBILE_T_150_1024")
        self.assertEquals(result["ticket_number"], self.contract.ticket_number)
        self.assertEquals(result["technology"],
                          self.contract.service_technology_id.name)
        self.assertEquals(result["supplier"], self.contract.service_supplier_id.name)
        self.assertEquals(result["lang"], self.contract.lang)
        self.assertEquals(
            result["iban"],
            self.contract.mandate_id.partner_bank_id.sanitized_acc_number
        )
        self.assertEquals(result["is_terminated"], self.contract.is_terminated)
        self.assertEquals(result["date_start"], self.contract.date_start)
        self.assertEquals(result["date_end"], self.contract.date_end)
        self.assertEquals(result["fiber_signal"], "fibraFTTH")
