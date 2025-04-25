from odoo import _, http
from odoo.exceptions import AccessError
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class PaymentController(CustomerPortal):
    @http.route(
        ["/my/banks"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_banks(self, **kw):
        partner = request.env.user.partner_id

        bank_accounts = (
            request.env["res.partner.bank"]
            .sudo()
            .search([("partner_id", "=", partner.id)])
        )

        values = {
            "page_name": "bank",
            "bank_accounts": bank_accounts,
        }

        return request.render(
            "account_banking_ach_direct_debit_portal.portal_banks", values
        )

    @http.route(
        ["/my/add-bank"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_add_bank(self, **kw):
        partner = request.env.user.partner_id

        if request.httprequest.method == "POST":
            bank = (
                request.env["res.bank"]
                .sudo()
                .create(
                    {
                        "name": kw.get("bank_name"),
                        "street": kw.get("bank_address"),
                    }
                )
            )

            request.env["res.partner.bank"].sudo().create(
                {
                    "acc_holder_name": kw.get("acc_holder_name"),
                    "acc_number": kw.get("acc_number"),
                    "bank_id": bank.id,
                    "aba_routing": kw.get("routing_number"),
                    "partner_id": partner.id,
                    "acc_type": kw.get("acc_type"),
                }
            )

            return request.redirect("/my/banks")

        acc_type_choices = request.env[
            "res.partner.bank"
        ]._get_supported_account_types()

        values = {
            "page_name": "bank",
            "acc_type_choices": acc_type_choices,
        }

        return request.render(
            "account_banking_ach_direct_debit_portal.portal_bank_form", values
        )

    @http.route(
        "/my/bank/delete/<int:bank_id>",
        type="http",
        auth="user",
        website=True,
        methods=["GET"],
    )
    def portal_delete_bank(self, bank_id, **kw):
        partner = request.env.user.partner_id
        partner_bank = request.env["res.partner.bank"].sudo().browse(bank_id)

        if not partner_bank.exists() or partner_bank.partner_id.id != partner.id:
            raise AccessError(
                _("You do not have permission to edit this bank account.")
            )

        bank = partner_bank.bank_id

        bank.unlink()
        partner_bank.unlink()

        return request.redirect("/my/banks")

    @http.route(
        "/my/bank/edit/<int:bank_id>",
        type="http",
        auth="user",
        website=True,
        methods=["GET", "POST"],
    )
    def portal_edit_bank(self, bank_id, **kw):
        partner = request.env.user.partner_id
        partner_bank = request.env["res.partner.bank"].sudo().browse(bank_id)

        if not partner_bank.exists() or partner_bank.partner_id.id != partner.id:
            raise AccessError(
                _("You do not have permission to edit this bank account.")
            )

        acc_type_choices = request.env[
            "res.partner.bank"
        ]._get_supported_account_types()

        if request.httprequest.method == "POST":
            bank = partner_bank.bank_id

            if bank:
                bank.sudo().write(
                    {
                        "name": kw.get("bank_name"),
                        "street": kw.get("bank_address"),
                    }
                )
            else:
                bank = (
                    request.env["res.bank"]
                    .sudo()
                    .create(
                        {
                            "name": kw.get("bank_name"),
                            "street": kw.get("bank_address"),
                        }
                    )
                )

            partner_bank.sudo().write(
                {
                    "acc_holder_name": kw.get("acc_holder_name"),
                    "acc_number": kw.get("acc_number"),
                    "bank_id": bank.id,
                    "aba_routing": kw.get("routing_number"),
                    "acc_type": kw.get("acc_type"),
                }
            )
            return request.redirect("/my/banks")

        return request.render(
            "account_banking_ach_direct_debit_portal.portal_bank_form",
            {
                "acc_type_choices": acc_type_choices,
                "bank": partner_bank,
                "edit_mode": True,
                "page_name": "bank",
            },
        )
