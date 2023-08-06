import json
import requests
from .auth import ShipdeoAuth
from .dto import BaseAddressDto, DestinationDto, ItemDto, OriginDto, ShippingPricing, TransactionDto, OrderDto

client_id = '7jgf8StrQRbuE8kJ'
client_secret = 'Eylh4kRbvz3PQNm1'

ShipdeoAuth(client_id=client_id, client_secret=client_secret)


class IShipping:

    def get_tariff(self, origin, destination, couriers=[], is_cod=False, items=None):
        pass

    def get_airwaybill_info(self, airwaybill: str):
        pass


class ShipdeoBaseService:
    
    def __init__(self, token, BASE_URL='https://main-api-production.shipdeo.com', request=None, is_prod=True) -> None:
        self.__token = token

        if is_prod:
            self._base_url = BASE_URL
        else:
            self._base_url = 'https://main-api-development.shipdeo.com'

        self._requests = request or requests
        self._headers = {
            'Authorization': 'Bearer ' + self.__token,
            'Content-Type': 'application/json'
        }

        super().__init__()


class ShipdeoTariffService(ShipdeoBaseService):

    def __build_payload_tariff(self, origin: BaseAddressDto, destination: BaseAddressDto, couriers, is_cod, items=None):
        return {
            "couriers": couriers,
            "is_cod": is_cod,
            "origin_lat": origin.lat,
            "origin_long": origin.long,
            "origin_province_name": origin.province_name,
            "origin_subdistrict_code": origin.subdistrict_code,
            "origin_subdistrict_name": origin.subdistrict_name,
            "origin_city_code": origin.city_code,
            "origin_city_name": origin.city_name,
            "origin_postal_code": origin.postal_code,
            "destination_lat": destination.lat,
            "destination_long": destination.long,
            "destination_province_name": destination.province_name,
            "destination_subdistrict_code": destination.subdistrict_code,
            "destination_subdistrict_name": destination.subdistrict_name,
            "destination_city_code": destination.city_code,
            "destination_city_name": destination.city_name,
            "destination_postal_code": destination.postal_code,
            "items": items,
            "isCallWeight": False
        }

    def get_tariff(self, origin: BaseAddressDto, destination: BaseAddressDto, couriers, is_cod, items=None):
       
        payload =  self.__build_payload_tariff(origin, destination, couriers, is_cod, items=items)
        respond = self._requests.post(self._base_url + '/v1/couriers/pricing', data=json.dumps(payload), headers=self._headers)
        
        results = []
        
        if respond.status_code == 200:
            for r in respond.json()['data']:
                shipping_price = ShippingPricing(r)
                results.append(shipping_price)
            return results
        elif respond.status_code == 401:
            print(respond.json())
            raise Exception(respond.json()['message'])
        else:
            raise Exception(respond.json())

    def get_couriers(self):
        respond = self._requests.get(self.__base_url + '/v1/couriers', headers=self.__headers)
        if respond.status_code == 200:
            return respond.json()
        

class ShipdeoServiceOrder(ShipdeoBaseService):

    def __build_payload_order(self, orderDto: OrderDto, transactionDto: TransactionDto, items=[]):
        return {
            "courier": orderDto.courier,
            "courier_service": orderDto.courier_service,
            "order_number": orderDto.order_number,
            "is_cod": orderDto.is_cod,
            "delivery_type": orderDto.delivery_type,
            "delivery_time": orderDto.delivery_time,
            "is_send_company": orderDto.is_send_company,
            "origin_lat": orderDto.origin_lat,
            "origin_long": orderDto.origin_long,
            "origin_subdistrict_code": orderDto.origin_subdistrict_code,
            "origin_subdistrict_name": orderDto.origin_subdistrict_name,
            "origin_city_code": orderDto.origin_city_code,
            "origin_city_name": orderDto.origin_city_name,
            "origin_province_code": orderDto.origin_province_code,
            "origin_province_name": orderDto.origin_province_name,
            "origin_contact_name": orderDto.origin_contact_name,
            "origin_contact_phone": orderDto.origin_contact_phone,
            "origin_contact_address": orderDto.origin_contact_address,
            "origin_contact_email": orderDto.origin_contact_email,
            "origin_note": orderDto.origin_note,
            "origin_postal_code": orderDto.origin_postal_code,
            "destination_lat": orderDto.destination_lat,
            "destination_long": orderDto.destination_long,
            "destination_subdistrict_code": orderDto.destination_subdistrict_code,
            "destination_subdistrict_name": orderDto.destination_subdistrict_name,
            "destination_city_code": orderDto.destination_city_code,
            "destination_city_name": orderDto.destination_city_name,
            "destination_province_code": orderDto.destination_province_code,
            "destination_province_name": orderDto.destination_province_name,
            "destination_postal_code": orderDto.destination_postal_code,
            "destination_contact_name": orderDto.destination_contact_name,
            "destination_contact_phone": orderDto.destination_contact_phone,
            "destination_contact_address": orderDto.destination_contact_address,
            "destination_contact_email": orderDto.destination_contact_email,
            "destination_note": orderDto.destination_note,
            "destination_company_name": orderDto.destination_company_name,
            "delivery_note": orderDto.delivery_note,
            "reference_number": orderDto.reference_number,
            "airwaybill_number": orderDto.airwaybill_number,
            "items": [
                {
                "name": item.name,
                "description": item.description,
                "weight": item.weight,
                "weight_uom": item.weight_uom,
                "qty": item.qty,
                "value": item.value,
                "width": item.width,
                "height": item.height,
                "length": item.length,
                "dimension_uom": item.dimension_uom,
                "total_value": item.total_value
                } for item in items
            ],
            "transaction": {
                "subtotal": transactionDto.subtotal,
                "shipping_charge": transactionDto.shipping_charge,
                "fee_insurance": transactionDto.fee_insurance,
                "is_insuranced": transactionDto.is_insuranced,
                "discount": transactionDto.discount,
                "total_value": transactionDto.total_value,
                "total_cod": transactionDto.total_cod,
                "weight": transactionDto.weight,
                "width": transactionDto.width,
                "height": transactionDto.height,
                "length": transactionDto.length,
                "coolie": transactionDto.coolie,
                "package_category": transactionDto.package_category,
                "package_content": transactionDto.package_content
            }
        }

    def create_order(self, orderDto: OrderDto, transactionDto: TransactionDto, items=[]):
        payload =  self.__build_payload_order(orderDto, transactionDto, items=items)
        return self._requests.post(self._base_url + '/v1/couriers/orders', data=json.dumps(payload), headers=self._headers)