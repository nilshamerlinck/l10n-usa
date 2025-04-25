# Copyright 2025 Kencove (https://www.kencove.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Banking ACH Direct Debit",
    "summary": "Account Banking ACH Direct Debit Portal",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Kencove, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-usa",
    "category": "Banking addons",
    "depends": ["account_banking_ach_direct_debit"],
    "data": [
        "views/autopay_rules_templates.xml",
        "views/banks_templates.xml",
        "views/breadcrumbs.xml",
        "views/homepage_templates.xml",
        "views/invoice_templates.xml",
        "views/payment_templates.xml",
        "views/searchbar.xml",
        "views/webclient_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "account_banking_ach_direct_debit_portal/static/src/scss/*.scss",
        ],
    },
    "installable": True,
}
