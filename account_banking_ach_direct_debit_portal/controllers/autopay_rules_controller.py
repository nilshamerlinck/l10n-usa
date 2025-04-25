import json
from datetime import date

from odoo import http
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class InvoiceController(CustomerPortal):
    @http.route(
        ["/autopay-rules"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_autopay_rules(self, **kw):
        current_date = date.today().strftime("%-m-%-d-%Y")

        values = {
            "page_name": "autopay_rules",
            "current_date": current_date,
            "partner": request.env.user.partner_id,
        }

        return request.render(
            "account_banking_ach_direct_debit_portal.portal_autopay_rules", values
        )

    @http.route(
        "/autopay-rules/change", type="http", auth="user", methods=["POST"], csrf=False
    )
    def update_autopay(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            autopay_value = data.get("autopay_rule")
        except Exception:
            return request.make_json_response({"error": "Invalid JSON"}, status=400)

        if autopay_value not in ["disabled", "end_of_month", "on_due_date"]:
            return request.make_json_response({"error": "Invalid value"}, status=400)

        partner = request.env.user.partner_id
        partner.sudo().write({"autopay": autopay_value})

        return request.make_json_response(
            {"status": "success", "autopay": autopay_value}
        )
