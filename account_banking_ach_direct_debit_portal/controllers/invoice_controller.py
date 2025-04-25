from odoo import _, http
from odoo.http import request

from odoo.addons.account.controllers.portal import PortalAccount
from odoo.addons.portal.controllers.portal import pager as portal_pager


class InvoiceController(PortalAccount):
    @http.route(
        ["/my/invoices", "/my/invoices/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_invoices(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search="",
        search_in="all",
        **kw
    ):
        values = self._prepare_my_invoices_values(
            page, date_begin, date_end, sortby, filterby
        )

        searchbar_inputs = {
            "all": {"label": _("All"), "input": "all"},
            "name": {"label": _("Invoice"), "input": "name"},
            "partner": {"label": _("Partner"), "input": "partner_id"},
        }

        domain = values.get("domain", [])
        if search:
            if search_in == "name":
                domain += [("name", "ilike", search)]
            elif search_in == "partner":
                domain += [("partner_id.name", "ilike", search)]
            else:
                domain += [
                    "|",
                    ("name", "ilike", search),
                    ("partner_id.name", "ilike", search),
                ]

        invoice_obj = request.env["account.move"].sudo()
        invoice_count = invoice_obj.search_count(domain)
        pager = portal_pager(
            url="/my/invoices",
            total=invoice_count,
            page=page,
            step=self._items_per_page,
            url_args={"date_begin": date_begin, "date_end": date_end},
        )
        invoices = invoice_obj.search(
            domain, limit=self._items_per_page, offset=pager["offset"]
        )

        request.session["my_invoices_history"] = invoices.ids[:100]

        values.update(
            {
                "invoices": invoices,
                "pager": pager,
                "search": search,
                "search_in": search_in,
                "searchbar_inputs": searchbar_inputs,
            }
        )

        return request.render(
            "account_banking_ach_direct_debit_portal.portal_custom_my_invoices", values
        )
