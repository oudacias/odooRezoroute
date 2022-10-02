from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class PackProducts(models.Model):
    _name = 'pack.products'

    product_id = fields.Many2one('product.product', string = 'Produits', required = True,
                               )
    product_tmpl_id = fields.Many2one('product.template', string = 'Produits')
    price = fields.Float('Prix', compute = 'compute_price', store = True)
    quantity = fields.Integer('Quantité', default = 1)
    product_variant = fields.Many2one('product.template', string = 'Produits')

    product_variant_ids1 = fields.One2many('product.template', 'variant_product','packs')


   
    @api.depends('product_id', 'quantity')
    def compute_price(self):
        for record in self:
            record.price = record.product_id.lst_price * record.quantity

    @api.onchange('quantity')
    def set_price(self):
        self.price = self.product_id.lst_price * self.quantity

    @api.constrains('quantity')
    def _check_positive_qty(self):
        if any([ml.quantity < 0 for ml in self]):
            raise ValidationError(_('Vous ne pouvez pas saisir une quantité négative'))




class ProductPack(models.Model):
    _inherit = 'product.template'
    is_pack = fields.Boolean('Un forfait ?')
    pack_price = fields.Integer(string = "Prix Forfait", store = True)
    pack_products_ids = fields.One2many('pack.products', 'product_tmpl_id', string = 'Produits du Forfait')

    variant_product = fields.Many2one('pack.products','packs', select=True) 

    test = []


    def write(self,vals):
        print("@@@@@@@@@ VIEW ID")
        
        if(self.env.context.get('view_id') == None):
            if self.env.user.has_group('ps_rezoroute.group_gestionnaire'):
                raise ValidationError(
                    ('Vous ne pouvez pas modifier un produit'),
                )
            else:
                return super(ProductPack, self).write(vals)
        else:
            (self.test).clear()
            (self.test).append(vals['pack_products_ids'])
        # return super(ProductPack, self).write(vals)


    
    
    def add_pack_order(self):  

        print("@@@@@@@@@@@@  SALE FORFAIT LINE")
        # print(self.test[0][0])  
        i = 0

        

        if(self.env.context.get('active_ids')):
            sale_forfait = self.env['sale.forfait'].create({
                                                'sale_id': self.env.context.get('active_ids'),
                                                'pack_id' :  self.env.context.get('product_product_id'),
                                            }) 


            for rec in self.pack_products_ids:
                if(len(self.test) > 0):
                    if(self.test[0][i][2] == False):
                        self.env['sale.forfait.line'].create({
                                                    'forfait_id' :  sale_forfait.id,
                                                    'product_line' : rec.product_id.id
                                                }) 
                    else:
                        self.env['sale.forfait.line'].create({
                                                    'forfait_id' :  sale_forfait.id,
                                                    'product_line' : self.test[0][i][2]['product_id']
                                                })
                else:
                    self.env['sale.forfait.line'].create({
                                                    'forfait_id' :  sale_forfait.id,
                                                    'product_line' : rec.product_id.id
                                                })

            
                i += 1

            product_product = self.env['product.product'].search([('id','=',self.env.context.get('product_product_id'))])

            name = product_product.display_name
            if product_product.description_sale:
                name += '\n' + product_product.description_sale


            self.env['sale.order.line'].create({
                'product_id': product_product.id,
                'price_unit': product_product.lst_price,
                'product_uom': product_product.uom_id.id,
                'product_uom_qty': 1,
                'order_id': self.env.context.get('active_ids'),
                'name': name,
                'tax_id' : product_product.taxes_id.ids,
                'forfait_id' : sale_forfait.id,
            })    



class SelectPack(models.TransientModel):
    _name = 'select.product.pack'

    product_id = fields.Many2one('product.product', string = 'Forfait ', domain = [('is_pack', '=', True)],
                                 required = True)


    product_id2 = fields.Many2one('product.template', string = 'Forfait ', domain = [('is_pack', '=', True)])
    quantity = fields.Integer('Quantité', default = 1, required = True)

    def add_pack_order(self):
        
        active_id = self._context.get('active_id')
        
        
        if active_id:
            sale_id = self.env['sale.order'].browse(active_id)
            name = self.product_id.display_name
            if self.product_id.description_sale:
                name += '\n' + self.product_id.description_sale
            self.env['sale.order.line'].create({
                'product_id': self.product_id.id,
                'price_unit': self.product_id.lst_price,
                'product_uom': self.product_id.uom_id.id,
                'product_uom_qty': self.quantity,
                'order_id': sale_id.id,
                'name': name,
                'tax_id' : self.product_id.taxes_id.ids,
            })

    @api.constrains('quantity')
    def _check_positive_qty(self):
        if any([ml.quantity < 0 for ml in self]):
            raise ValidationError(_('Vous ne pouvez pas saisir une quantité négative'))

    def update_products_pack(self):
        print("@@@@@@@@@@@@ TEMPLATE")
        print(self.product_id.product_tmpl_id.pack_products_ids)
        print(self._context.get('active_id'))
        self.ensure_one()
        return {

                    'view_id': self.env.ref('ps_rezoroute.product_pack_template_form').id,
                    'type': 'ir.actions.act_window',
                    'res_model': 'product.template',
                    'view_mode': 'form',
                    'res_id': self.product_id.product_tmpl_id.id,
                    'target': 'new',
                    'context' : {
                        'create' : False,
                        'active_ids': self._context.get('active_id'),
                        'product_product_id' : self.product_id.id,
                        'view_id': self.env.ref('ps_rezoroute.product_pack_template_form').name,

                    },
                }


        
class SaleForfait(models.Model):
    _name = 'sale.forfait'

    sale_id = fields.Many2one('sale.order')
    pack_id = fields.Many2one('product.product', string = 'Forfait ', domain = [('is_pack', '=', True)],
                                 required = True)

class SaleForfaitLine(models.Model):
    _name = 'sale.forfait.line'

    forfait_id = fields.Many2one('sale.forfait')
    product_line = fields.Many2one('product.template')

class SaleLineForfait(models.Model):

    _inherit = 'sale.order.line'

    forfait_id = fields.Many2one('sale.forfait')
    is_forfait = fields.Boolean()



class SaleForfaitCount(models.Model):
    _inherit = 'sale.order'
    picking_forfait_ids = fields.One2many('stock.picking','forfait_sale')
    delivery_forfait_count = fields.Integer(compute='_compute_forfait_picking_ids')

    @api.depends('picking_ids')
    def _compute_forfait_picking_ids(self):
        for order in self:
            order.delivery_forfait_count = len(order.picking_forfait_ids)

    def get_action_view_picking_forfait(self):
        pickings = self.picking_forfait_ids
        '''
        This function returns an action that display existing delivery orders
        of given sales order ids. It can either be a in a list or in a form
        view, if there is only one delivery order to show.
        '''
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")

        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif pickings:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.id
        # Prepare the context.
        picking_id = pickings.filtered(lambda l: l.picking_type_id.code == 'outgoing')
        if picking_id:
            picking_id = picking_id[0]
        else:
            picking_id = pickings[0]
        action['context'] = dict(self._context, default_partner_id=self.partner_id.id, default_picking_type_id=picking_id.picking_type_id.id, default_origin=self.name, default_group_id=picking_id.group_id.id)
        return action

    