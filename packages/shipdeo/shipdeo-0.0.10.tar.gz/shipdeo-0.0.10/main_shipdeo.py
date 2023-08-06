from shipdeo.auth import ShipdeoAuth
from shipdeo.shipping import ShipdeoTariffService, ShipdeoServiceOrder
from shipdeo.dto import DestinationDto, OrderDto, OriginDto, ItemDto, TransactionDto

client_id = 'gCVj5Yr51m7eWJiJ'
client_secret = 'IkJ6Kbl0vGbK9XVK'

def create_order(shipdeo: ShipdeoServiceOrder):
    orderDto = OrderDto()
    orderDto.courier = "sicepat"
    orderDto.courier_service = "best"
    orderDto.order_number = "RMD000001"
    orderDto.is_cod = False
    orderDto.delivery_type = "dropoff"
    orderDto.is_send_company = False
    orderDto.origin_subdistrict_code = "32.77.01"
    orderDto.origin_subdistrict_name = "CIMAHI SELATAN"
    orderDto.origin_city_code = "32.77"
    orderDto.origin_city_name = "KOTA CIMAHI"
    orderDto.origin_province_code = "32"
    orderDto.origin_province_name = "JAWA BARAT"
    orderDto.origin_contact_name = "John Doe"
    orderDto.origin_contact_phone = "08123456789"
    orderDto.origin_contact_address = "Jl. Raya Cibiru No. 123"
    orderDto.origin_contact_email = "john.doe@example.com"
    orderDto.origin_note = "Note for origin address"
    orderDto.destination_subdistrict_code = "32.77.01"
    orderDto.destination_subdistrict_name = "CIMAHI SELATAN"
    orderDto.destination_city_code = "32.77"
    orderDto.destination_city_name = "KOTA CIMAHI"
    orderDto.destination_province_code = "32"
    orderDto.destination_province_name = "JAWA BARAT"
    orderDto.destination_contact_name = "Jane Doe"
    orderDto.destination_contact_phone = "08123456789"
    orderDto.destination_contact_address = "Jl. Raya Pondok Kelapa No. 456"
    orderDto.destination_contact_email = "jane.doe@example.com"
    orderDto.destination_note = "Note for destination address"
    orderDto.destination_company_name = "Destination Company"
    orderDto.delivery_note = "Delivery note"

    transactionDto = TransactionDto()
    transactionDto.subtotal = 500000
    transactionDto.shipping_charge = 25000
    transactionDto.fee_insurance = 15000
    transactionDto.is_insuranced = True
    transactionDto.discount = 100000
    transactionDto.total_value = 465000
    transactionDto.total_cod = 0
    transactionDto.weight = 2.5
    transactionDto.width = 30
    transactionDto.height = 20
    transactionDto.length = 40
    transactionDto.coolie = 1
    transactionDto.package_category = "Express"
    transactionDto.package_content = "Electronic Devices"

    items = []
    item = ItemDto()
    item.weight = 10
    item.description = 'baju'
    item.dimension_uom = 'cm'
    item.height = 0 
    item.width = 0 
    item.is_wood_package = False
    item.length = 0
    item.name = 'SKU001'
    item.qty = 10
    item.value = 10000
    item.weight = 8
    item.weight_uom = 'gram'
    item.total_value = 100000
    items.append(item)

    shipdeo.create_order(orderDto, transactionDto, items)


if __name__ == '__main__':
    token = "7c6c5c1747e2fe6c1ffdad12f8c7ad425978c962"
    shipdeo = ShipdeoServiceOrder(token)
    create_order(shipdeo)

def cek_ongkir():
    auth = ShipdeoAuth(client_id=client_id, client_secret=client_secret)
    # print(auth.get_token())

    token = "7c6c5c1747e2fe6c1ffdad12f8c7ad425978c962"
    shipdeo = ShipdeoTariffService(token)

    origin = OriginDto()
    origin.subdistrict_code = "32.77.01"
    origin.subdistrict_name = "CIMAHI SELATAN1"
    origin.city_code = "32.77"
    origin.city_name = "CIMAHI1"
    origin.province_code = "32"
    origin.province_name = "JAWA BARAT1"
    origin.postal_code = "40532"


    destination = DestinationDto()
    destination.subdistrict_code = "32.77.02"
    destination.subdistrict_name = "CIMAHI SELATAN2"
    destination.city_code = "32.77"
    destination.city_name = "CIMAHI1"
    destination.province_code = "we"
    destination.province_name = "JAWA BARAT2"
    destination.postal_code = "40532"

    items = []
    item = ItemDto()
    item.weight = 10
    item.description = 'baju'
    item.dimension_uom = 'cm'
    item.height = 0 
    item.width = 0 
    item.is_wood_package = False
    item.length = 0
    item.name = 'SKU001'
    item.qty = 10
    item.value = 10000
    item.weight = 8
    item.weight_uom = 'gram'



    items.append(item.__dict__)
    # try:
    result = shipdeo.get_tariff(origin=origin, destination=destination, couriers=["sap","sicepat"], is_cod=False, items=items)

    for r in result:
        # print(r.courier, r.service)
        print(r)

