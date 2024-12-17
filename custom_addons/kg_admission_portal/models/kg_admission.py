from odoo import models, fields, api
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)
import json
import requests

class KGAdmission(models.Model):
    _name = 'kg.admission'
    _description = 'KG Admission Form'

    child_name = fields.Char(string='Child Name', required=True)
    dob = fields.Date(string='Date of Birth', required=True)
    parent_name = fields.Char(string='Parent/Guardian Name', required=True)
    contact_number = fields.Char(string='Contact Number', required=True)
    email = fields.Char(string='Email', required=True)
    address = fields.Text(string='Address')
    grade = fields.Selection([
        ('pre_kg', 'Pre-KG'),
        ('lower_kg', 'Lower KG'),
        ('upper_kg', 'Upper KG')
    ], string='Grade', required=True)
    documents = fields.Binary(string='Upload Documents')
    document_name = fields.Char(string="Document Name")
    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], string='Payment Status', default='pending')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft')

    @api.model
    def create(self, vals):
        vals['state'] = 'submitted'
        self._send_notifications(vals)
        return super(KGAdmission, self).create(vals)

    def _send_notifications(self, vals):
        email_template = self.env.ref('kg_admission_portal.email_template_admission_ack')
        if email_template:
            email_template.sudo().send_mail(self.id, force_send=True)
        # Add SMS gateway integration here if needed
