from odoo import api, models
import re
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    @api.constrains('phone')
    def phone_validator(self):
        if self.phone:
            match = re.match(r'^\+?[0-9\s\-\(\)]{10,16}$', self.phone)
            if match is None:
                raise ValidationError('Telefono no valido')
            
    @api.constrains('mobile')
    def mobil_validator(self):
        if self.mobile:
            match = re.match(r'^\+?[0-9\s\-\(\)]{10,16}$', self.mobile)
            if match is None:
                raise ValidationError('Telefono no valido')