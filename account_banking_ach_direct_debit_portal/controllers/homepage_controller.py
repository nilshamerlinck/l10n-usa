from odoo import _, http
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class HomepageController(CustomerPortal):
    def _get_invoices_domain(self):
        return [
            ("state", "not in", ("cancel", "draft")),
            (
                "move_type",
                "in",
                (
                    "out_invoice",
                    "out_refund",
                    "in_invoice",
                    "in_refund",
                    "out_receipt",
                    "in_receipt",
                ),
            ),
        ]

    def _get_invoice_searchbar_sortings(self):
        return {
            "lastest": {"label": _("Lastest"), "order": "date desc"},
            "oldest": {"label": _("Oldest"), "order": "date"},
        }

    def _get_payment_searchbar_sortings(self):
        return {
            "lastest": {"label": _("Lastest"), "order": "date desc"},
            "oldest": {"label": _("Oldest"), "order": "date"},
        }

    def _prepare_homepage_layout_values(
        self, invoice_sortby=None, payment_sortby=None, **kw
    ):
        values = self._prepare_portal_layout_values()

        invoice_searchbar_sortings = self._get_invoice_searchbar_sortings()
        payment_searchbar_sortings = self._get_payment_searchbar_sortings()

        if not invoice_sortby:
            invoice_sortby = "lastest"

        if not payment_sortby:
            payment_sortby = "lastest"

        values.update(
            {
                "invoice_searchbar_sortings": invoice_searchbar_sortings,
                "payment_searchbar_sortings": payment_searchbar_sortings,
                "invoice_sortby": invoice_sortby,
                "payment_sortby": payment_sortby,
            }
        )

        return values

    @http.route(["/my", "/my/home"], type="http", auth="user", website=True)
    def home(self, invoice_sortby=None, payment_sortby=None, **kw):
        values = self._prepare_homepage_layout_values(invoice_sortby, payment_sortby)

        invoices = request.env["account.move"].search(
            self._get_invoices_domain(),
            order="date desc" if values["payment_sortby"] == "lastest" else "date",
            limit=5,
        )

        payments = request.env["account.payment"].search(
            [],
            order="invoice_date desc"
            if values["payment_sortby"] == "lastest"
            else "invoice_date",
            limit=5,
        )

        values.update(
            {
                "invoices": invoices,
                "payments": payments,
            }
        )

        return request.render(
            "account_banking_ach_direct_debit_portal.portal_my_home", values
        )
