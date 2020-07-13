# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    # region Fields
    ecofi_validations_enabled = fields.Boolean(
        string='Enabled Validations',
        default=True,
    )
    ecofi_validation_id = fields.Many2one(
        comodel_name='ecofi.validation',
        domain="[('id', '=', id)]",
        required=True,
        copy=False,
        ondelete='cascade',
        delegate=True,
    )
    journal_ids = fields.Many2many(
        comodel_name='account.journal',
        relation='res_company_account_journal',
        column1='res_company_id',
        column2='account_journal_id',
        string='Default Journals',
        check_company=True,
    )
    # endregion

    # region Business Methods
    def uses_skr(self):
        return self.chart_template_id.name in [
            'Deutscher Kontenplan SKR03',
            'Deutscher Kontenplan SKR04',
        ]
    # endregion

    @api.model
    def create(self, vals):
        vals['ecofi_validation_id'] = self.ecofi_validation_id.create({}).id
        res = super(ResCompany, self).create(vals)
        res.ecofi_validation_id.write({
            'company_id': res.id,
        })
        return res
