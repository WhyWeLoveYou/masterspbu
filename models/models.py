# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class AkumulasiData(models.Model):
    _name = 'master_spbu.akumulasidata'
    _description = 'master_spbu.akumulasidata'

    def action_confirm(self):
        if self.status == 'draft':
            self.status = 'confirmed'

    def action_draft(self):
        if self.status == 'confirmed':
            self.status = 'draft'

    def action_done(self):
        if self.status == 'confirmed':
            self.status = 'done'
    
    tanggal = fields.Date(string='Tanggal Mulai')
    sampai_tanggal = fields.Date(string='Tanggal Selesai')
    month_year = fields.Char(string='Name', compute='_compute_month_year')
    status = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done')], string='Status', default='draft')
    total_loses = fields.Float(related='akumulasidata_line_ids.loses', string='Total Loses', store=True)
    total_rupiah = fields.Float(related='akumulasidata_line_ids.rupiah', string='Total Rupiah', store=True)
    akumulasidata_line_ids = fields.One2many('master_spbu.akumulasidata_line', 'akumulasidata_ids', string='Line Items')

    @api.depends('tanggal')
    def _compute_month_year(self):
        for record in self:
            if record.tanggal:
                record.month_year = record.tanggal.strftime('%B %Y')
            else:
                record.month_year = ''

    @api.constrains('tanggal', 'sampai_tanggal')
    def _check_tanggal(self):
        for record in self:
            if record.tanggal and record.sampai_tanggal and record.tanggal > record.sampai_tanggal:
                raise ValidationError('Tanggal Mulai tidak bisa lebih dari Tanggal Selesai.')
                self.status = 'draft'

class Stock(models.Model):
    _name = 'master_spbu.stock'
    _description = 'master_spbu.stock'

    name = fields.Char(string='Name')
    tanggal = fields.Date(string='Tanggal')
    stock_line_ids = fields.One2many('master_spbu.stock_line', 'stock_ids', string='stock Line Items')

class Premium3(models.Model):
    _name = 'master_spbu.premium3'
    _description = 'master_spbu.premium3'

    name = fields.Char(string='Name')
    tanggal = fields.Date(string='Tanggal')
    premium3_line_ids = fields.One2many('master_spbu.premium3_line', 'premium3_ids', string='Premium3 Line Items')


class AkumulasiDataLine(models.Model):
    _name = 'master_spbu.akumulasidata_line'
    _description = 'master_spbu.akumulasidata_line'

    def _compute_laku(self):
        for line in self:
            line.laku = line.t1 + line.t2 + line.t3 + line.t4

    def _compute_rupiah(self):
        for line in self:
            line.rupiah = line.laku * 7250

    @api.depends('stock_awal', 'kiriman', 'laku')
    def _compute_stock_akhir(self):
        for line in self:
            line.stock_akhir = line.stock_awal + line.kiriman - line.laku
            
    @api.depends('stock_tangki', 'stock_akhir')
    def _compute_selisih(self):
        for line in self:
            line.selisih = line.stock_tangki - line.stock_akhir
            if line.selisih < 0:
                line.selisih = abs(line.selisih)

    @api.depends('selisih')
    def _compute_total(self):
        for line in self:
            line.akumulasi = line.selisih
            
    @api.depends('akumulasidata_ids', 'selisih')
    def _compute_loses(self):
        for record in self:
            record.loses = sum(line.selisih for line in record.akumulasidata_ids.akumulasidata_line_ids)

    akumulasidata_ids = fields.Many2one('master_spbu.akumulasidata', string='Akumulasi Data')
    tanggal = fields.Char(string='Tanggal')
    stock_awal = fields.Float(string='Stock Awal', default=0.0)
    kiriman = fields.Float(string='Kiriman', default=0.0)
    tera = fields.Float(string='Tera', default=0.0)
    t1 = fields.Float(string='T1', default=0.0)
    t2 = fields.Float(string='T2', default=0.0)
    t3 = fields.Float(string='T3', default=0.0)
    t4 = fields.Float(string='T4', default=0.0)
    laku = fields.Float(string='Laku', default=0.0, compute=_compute_laku)
    rupiah = fields.Float(string='Rupiah', default=0.0, compute=_compute_rupiah)
    stock_akhir = fields.Float(string='Stock Akhir', default=0.0, compute=_compute_stock_akhir)
    stock_tangki = fields.Float(string='Stock Tangki', default=0.0)
    selisih = fields.Float(string='Selisih', default=0.0, compute=_compute_selisih)
    akumulasi = fields.Float(string='Akumulasi', default=0.0, compute=_compute_total)
    loses = fields.Float(string='Loses', default=0.0, compute=_compute_loses)
    parent_status = fields.Selection(related='akumulasidata_ids.status', string='Status', store=True)
            

class StockLine(models.Model):
    _name = 'master_spbu.stock_line'
    _description = 'master_spbu.stock_line'

    stock_ids = fields.Many2one('master_spbu.stock', string='stock')
    tanggal = fields.Char(string='Tanggal')
    doa_awal = fields.Float(string='doa awal', default=0.0)
    tebusan = fields.Float(string='tebusan', default=0.0)
    kiriman = fields.Float(string='kiriman', default=0.0)
    sisa_do = fields.Float(string='sisa do', default=0.0)

class Premium3Line(models.Model):
    _name = 'master_spbu.premium3_line'
    _description = 'master_spbu.premium3_line'

    premium3_ids = fields.Many2one('master_spbu.premium3', string='Premium3')
    tanggal = fields.Char(string='Tanggal')
    premium = fields.Float(string='Premium', default=0.0)
    solar = fields.Float(string='Solar', default=0.0)
    pertamax = fields.Float(string='Pertamax', default=0.0)
    pertalite = fields.Float(string='Pertalite', default=0.0)
    dexlite = fields.Float(string='Dexlite', default=0.0)

    total = fields.Float(string='Total Tebusan', compute='_compute_total_tebusan')

    @api.depends('premium', 'solar', 'pertamax', 'pertalite', 'dexlite')
    def _compute_total_tebusan(self):
        for record in self:
            record.total = record.premium + record.solar + record.pertamax + record.pertalite + record.dexlite


