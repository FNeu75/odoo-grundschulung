# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    # create ecofi.validation data for companies
    env = api.Environment(cr, SUPERUSER_ID, {})

    for company in env['res.company'].search([]):
        env['ecofi.validation'].create({
            'company_id': company.id,
        })
