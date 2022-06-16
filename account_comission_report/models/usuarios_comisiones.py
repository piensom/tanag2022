# -*- coding: utf-8 -*-
# Copyright 2021 PIENSOM
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models, api, _

class UsuariosComisiones(models.Model):
    _name = "usuarios.comisiones"

    nombre = fields.Char(
        string='Nombre',
    )

    porcentaje = fields.Float(
        string='Porcentaje',
    )

    activo = fields.Boolean(
        string='Activo',
    )

