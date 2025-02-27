from core.models import Item


def create_line_item_dict(item: Item, amount: int = 1, tax_id: str = None):
    item_dict = {
        'price_data': {
            'currency': item.currency.iso_code,
            'product_data': {
                'name': item.name,
            },
            'unit_amount': item.price * 100,
        },
        'quantity': amount,
    }
    if tax_id:
        item_dict['tax_rates'] = [tax_id]
    
    return item_dict
