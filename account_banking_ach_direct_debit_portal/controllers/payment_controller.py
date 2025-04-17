from odoo import _, fields, http
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class PaymentController(CustomerPortal):
    @http.route(
        ["/my/payments", "/my/payments/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_payments(
        self, page=1, sortby=None, filterby=None, search="", search_in="all", **kw
    ):
        ScheduledPayment = request.env["account.payment"]

        searchbar_inputs = {
            "all": {"label": _("All"), "input": "all"},
            "partner": {"label": _("Amount"), "input": "amount_total"},
        }

        # -- Filters
        filter_options = {
            "all": {"label": _("All"), "domain": []},
            "future": {
                "label": _("Upcoming"),
                "domain": [("scheduled_date", ">=", fields.Date.today())],
            },
            "past": {
                "label": _("Past"),
                "domain": [("scheduled_date", "<", fields.Date.today())],
            },
        }

        domain = []

        if filterby in filter_options:
            domain += filter_options[filterby]["domain"]
        else:
            filterby = "all"

        # -- Search
        if search:
            if search_in == "partner":
                domain += [("bank_partner_id.name", "ilike", search)]
            else:
                domain += [
                    "|",
                    ("name", "ilike", search),
                    ("bank_partner_id.name", "ilike", search),
                ]

        # -- Count & pager
        total = ScheduledPayment.search_count([])
        pager = portal_pager(
            url="/my/payments",
            total=total,
            page=page,
            step=20,
            url_args={"sortby": sortby, "filterby": filterby, "search": search},
        )

        payments = ScheduledPayment.search([], offset=pager["offset"], limit=20)

        values = {
            "payments": payments,
            "page_name": "schedule_payment",
            "pager": pager,
            "default_url": "/my/payments",
            "searchbar_filters": filter_options,
            "sortby": sortby,
            "filterby": filterby,
            "search": search,
            "search_in": search_in,
            "searchbar_inputs": searchbar_inputs,
        }

        return request.render(
            "account_banking_ach_direct_debit_portal.portal_scheduled_payments", values
        )

    @http.route(
        "/payment",
        type="http",
        auth="user",
        website=True,
        methods=["GET", "POST"],
    )
    def payment(self, **kw):
        values = {
            "page_name": "payment",
        }

        return request.render(
            "account_banking_ach_direct_debit_portal.portal_payment", values
        )

    @http.route(
        "/manual-payment",
        type="http",
        auth="user",
        website=True,
        methods=["GET", "POST"],
    )
    def manual_payment(self, **kw):
        values = {
            "page_name": "manual_payment",
        }

        return request.render(
            "account_banking_ach_direct_debit_portal.portal_manual_payment", values
        )

    @http.route(
        "/select-payment-method",
        type="http",
        auth="user",
        website=True,
        methods=["GET", "POST"],
    )
    def select_payment_method(self, **kw):
        values = {
            "page_name": "select_payment_method",
        }

        return request.render(
            "account_banking_ach_direct_debit_portal.portal_select_payment_method",
            values,
        )
