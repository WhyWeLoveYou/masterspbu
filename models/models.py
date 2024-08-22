# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Premium(models.Model):
    _name = 'master_spbu.premium'
    _description = 'master_spbu.premium'

    name = fields.Char(string='Name')
    tanggal = fields.Date(string='Tanggal')
    premium_line_ids = fields.One2many('master_spbu.premium_line', 'premium_ids', string='Line Items')

class Premium2(models.Model):
    _name = 'master_spbu.premium2'
    _description = 'master_spbu.premium2'

    name = fields.Char(string='Name')
    tanggal = fields.Date(string='Tanggal')
    premium2_line_ids = fields.One2many('master_spbu.premium2_line', 'premium2_ids', string='Premium2 Line Items')

class PremiumLine(models.Model):
    _name = 'master_spbu.premium_line'
    _description = 'master_spbu.premium_line'

    def _laku(self):
        for line in self:
            line.laku = line.t1 + line.t2 + line.t3 + line.t4

    def _rupiah(self):
        for line in self:
            line.rupiah = line.laku * 7250

    def _stock_akhir(self):
        for line in self:
            line.stock_akhir = line.stock_awal + line.kiriman - line.laku

    def _selisih(self):
        for line in self:
            line.selisih = line.stock_tangki - line.stock_akhir
            if line.selisih < 0:
                line.selisih = line.selisih * -1

    def _total(self):
        for line in self:
            line.akumulasi = line.selisih * 1
    
    premium_ids = fields.Many2one('master_spbu.premium', string='Premium')
    tanggal = fields.Char(string='Tanggal')
    stock_awal = fields.Float(string='Stock Awal', default=0.0)
    kiriman = fields.Float(string='Kiriman', default=0.0)
    tera = fields.Float(string='Tera', default=0.0)
    t1 = fields.Float(string='T1', default=0.0)
    t2 = fields.Float(string='T2', default=0.0)
    t3 = fields.Float(string='T3', default=0.0)
    t4 = fields.Float(string='T4', default=0.0)
    laku = fields.Float(string='Laku', default=0.0, compute=_laku)
    rupiah = fields.Float(string='Rupiah', default=0.0, compute=_rupiah)
    stock_akhir = fields.Float(string='Stock Akhir', default=0.0, compute=_stock_akhir)
    stock_tangki = fields.Float(string='Stock Tangki', default=0.0)
    selisih = fields.Float(string='Selisih', default=0.0, compute=_selisih)
    akumulasi = fields.Float(string='Akumulasi', default=0.0, compute=_total)

class Premium2Line(models.Model):
    _name = 'master_spbu.premium2_line'
    _description = 'master_spbu.premium2_line'

    premium2_ids = fields.Many2one('master_spbu.premium2', string='Premium2')
    tanggal = fields.Char(string='Tanggal')
    doa_awal = fields.Float(string='doa awal', default=0.0)
    tebusan = fields.Float(string='tebusan', default=0.0)
    kiriman = fields.Float(string='kiriman', default=0.0)
    sisa_do = fields.Float(string='sisa do', default=0.0)

