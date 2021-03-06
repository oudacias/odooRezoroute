from odoo import fields, models

class Vehicle(models.Model):

    _inherit = 'fleet.vehicle'
    siv = fields.Char(string="SIV")
    manufacturer_id = fields.Many2one('engine.manufacturer','Constructeur')
    code_moteur = fields.Many2one('engine.motor','Code moteur')
    type_id = fields.Many2one('engine.type','Type')
    d_2_1 = fields.Char(string="D2.1")
    e = fields.Char(string="E/VIN")
    note = fields.Text(string="Note Interne")
    partner_id = fields.Many2one('res.partner','Client')
    last_buy = fields.Date(string="Date dernier achat")
    last_servicing_date = fields.Date(string="Date derniere revision")
    odometer = fields.Integer(string="Dernier releve kilometrique")


class EngineMotor(models.Model):
    _name = 'engine.motor'

    manufacturer_id = fields.Many2one('engine.manufacturer','Manufacturer')

    name = fields.Char(string="Name")
    tecdoc_ref = fields.Char(string="TecDoc Ref")
    active = fields.Boolean(string="Active")
    note = fields.Text()


class EngineManufacturer(models.Model):
    _name = "engine.manufacturer"

    name = fields.Char(string="Nom")
    is_favourite = fields.Boolean(string="Favoris")
    tecdoc_ref = fields.Char(string="Reference TecDoc")
    tec_doc_supplier_ref = fields.Char(string="Reference Marque TecDoc")
    is_pkw = fields.Boolean(string="VL")
    is_nkw = fields.Boolean(string="PL")
    is_vgl = fields.Boolean(string="Marque") 
    active = fields.Boolean(string="Actif")
    sequence = fields.Integer(string="Sequence")
    m_code = fields.Char(string="M Code")
    m_code_reconditionned = fields.Char(string="M Code Reconditionne")
    m_code_f1 = fields.Char(string="M Code F1")
    m_code_agra = fields.Char(string="M Code AGRA")
    suffix_echange_standard = fields.Char(string="Suffixe Echange Standard")

    engine_list = fields.Many2many("engin.manufacturer.golda","golda_engine_rel","engine_id","golda_id",string="Golda",default_order="name asc")



    use_product_price = fields.Selection([('customer','Prix public'),('supplier','Prix fournisseur')],'Prix Golda prefere')
    supplier_code= fields.Char(string="Supplier Code")

    picture_url = fields.Image('Image')


class EngineType(models.Model):
    _name="engine.type"
    
    name = fields.Char(string="Nom")
    subtype_txt = fields.Char(string="Sous type (PL)")
    tecdoc_ref = fields.Char(string="Reference TecDoc")
    tecdoc_ref_nkw = fields.Char(string="TecDoc Ref CV")
    active = fields.Boolean(string="Actif")
    date_from = fields.Date(string="De")
    date_to = fields.Date(string="A")
    ccm_tax = fields.Integer(string="CC Tax")
    ccm_tech = fields.Integer(string="CC Tech")
    nb_cylinder = fields.Integer(string="Cylindree")
    motor_Code_txt = fields.Char(string="Code(s) moteur(s)")
    output_kw = fields.Integer(string="KW")
    ccm_lit = fields.Integer(string="Engine Capacity L")
    fuel_tank = fields.Integer(string="Fuel Tank")
    nb_doors = fields.Integer(string="Doors")
    voltage = fields.Integer(string="Voltage")
    abs = fields.Selection([('yes','Oui'),('no','Non'),('optional','Optionnel')],string='ABS')
    asr = fields.Selection([('yes','Oui'),('no','Non'),('optional','Optionnel')],string='ASR')
    valves = fields.Integer(string="Valves")
    motor_type_id = fields.Many2one('engine.motor.type','Motor Type')
    propulsion_id = fields.Many2one('engine.propulsion','Propulsion')
    injector_id = fields.Many2one('engine.injector','Injector')
    brake_system_id = fields.Many2one('engine.brake.system','Brake System')
    brake_type_id = fields.Many2one('engine.brake.type','Brake Type')
    catalyst_id = fields.Many2one('engine.catalyst','Catalyst')
    gear_id = fields.Many2one('engine.gear','Gear')    
    
    carosserie_id = fields.Many2one('engine.carosserie','Carosserie')







class EngineMotorType(models.Model):
    _name="engine.motor.type"

    name = fields.Char(string="Nom")
    tecdoc_ref = fields.Char(string="TecDoc Ref")
    sort = fields.Integer(string="Sort")
    active = fields.Boolean(string="Active")


class EnginePropulsion(models.Model):
    _name="engine.propulsion"

    name = fields.Char(string="Nom")
    tecdoc_ref = fields.Char(string="TecDoc Ref")
    sort = fields.Integer(string="Sort")
    active = fields.Boolean(string="Active")


class EngineInjector(models.Model):
    _name="engine.injector"

    sort = fields.Integer(string="Sort")
    note = fields.Text(string="Note Interne")
    tecdoc_ref = fields.Char(string="TecDoc Ref")
    name = fields.Char(string="Nom")
    active = fields.Boolean(string="Active")


class EngineCarosserie(models.Model):
    _name="engine.carosserie"

    name = fields.Char(string="Nom")
    tecdoc_ref = fields.Char(string="TecDoc Ref")
    sort = fields.Integer(string="Sort")
    active = fields.Boolean(string="Active")
    note = fields.Text(string="Note")

class EngineBrakeSystem(models.Model):
    _name="engine.brake.system"

    name = fields.Char(string="Nom")
    tecdoc_ref = fields.Char(string="TecDoc Ref")
    sort = fields.Integer(string="Sort")
    active = fields.Boolean(string="Active")
    note = fields.Text(string="Note")


class EngineBrakeType(models.Model):
    _name="engine.brake.type"

    name = fields.Char(string="Nom")
    tecdoc_ref = fields.Char(string="TecDoc Ref")
    sort = fields.Integer(string="Sort")
    active = fields.Boolean(string="Active")
    note = fields.Text(string="Note")

class EngineCatalyst(models.Model):
    _name="engine.catalyst"

    name = fields.Char(string="Nom")
    tecdoc_ref = fields.Char(string="TecDoc Ref")
    sort = fields.Integer(string="Sort")
    active = fields.Boolean(string="Active")
    note = fields.Text(string="Note")

class EngineGear(models.Model):
    _name="engine.gear"

    name = fields.Char(string="Nom")
    tecdoc_ref = fields.Char(string="TecDoc Ref")
    sort = fields.Integer(string="Sort")
    active = fields.Boolean(string="Active")
    note = fields.Text(string="Note")










