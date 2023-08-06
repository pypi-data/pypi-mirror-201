import json

class BaseAddressDto:
    lat = None
    long = None
    province_name = None
    province_code = None
    subdistrict_code = None
    subdistrict_name = None
    city_code = None
    city_name = None
    postal_code = None

class OriginDto(BaseAddressDto):
    pass

class DestinationDto(BaseAddressDto):
    pass

class ShippingPricing:
    courier = None
    courier_code = None
    service = None
    price = None
    duration = None
    support_cod = False
    estimation = None
    insurance_value = None
    return_rate = None
    return_level = None

    def __init__(self, data: json) -> None:
        self.courier = data['courier']
        self.courier_code = data['courierCode']
        self.service = data['service']
        self.price = data['price']
        self.duration = data['duration']
        self.support_cod = data['supportCod']
        self.estimation = data['estimation']
        self.insurance_value = data['insuranceValue']
        self.return_rate = data['returnRate']
        self.return_level = data['returnLevel']
    
    def __repr__(self) -> str:
        return "{} {} {}".format(self.courier, self.service, self.price)

class ItemDto:
    name = None
    description = None
    weight = None
    weight_uom = None
    qty = 1
    value = 0
    width = 0
    height = 0
    length = 0
    is_wood_package = False
    dimension_uom = None
    total_value = 0

    def to_json(self):
        return json.dumps(self.__dict__)

class OrderDto:
    courier = None
    service = None
    order_number = None
    is_cod = None
    delivery_type = None
    delivery_time = None
    is_send_company = None
    origin_lat = None
    origin_long = None
    origin_subdistrict_code = None
    origin_subdistrict_name = None
    origin_city_code = None
    origin_city_name = None
    origin_province_code = None
    origin_province_name = None
    origin_contact_name = None
    origin_contact_phone = None
    origin_contact_address = None
    origin_contact_email = None
    origin_note = None
    origin_postal_code = None
    destination_lat = None
    destination_long = None
    destination_subdistrict_code = None
    destination_subdistrict_name = None
    destination_city_code = None
    destination_city_name = None
    destination_province_code = None
    destination_province_name = None
    destination_postal_code = None
    destination_contact_name = None
    destination_contact_phone = None
    destination_contact_address = None
    destination_contact_email = None
    destination_note = None
    destination_company_name = None
    delivery_note = None
    reference_number = None
    airwaybill_number = None

class TransactionDto:
    def __init__(self):
        self.subtotal = None
        self.shipping_charge = None
        self.fee_insurance = None
        self.is_insuranced = None
        self.discount = None
        self.total_value = None
        self.total_cod = None
        self.weight = None
        self.width = None
        self.height = None
        self.length = None
        self.coolie = None
        self.package_category = None
        self.package_content = None
