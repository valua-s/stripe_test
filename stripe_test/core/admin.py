from django.contrib import admin

from .models import Currency, Item, Discount, Tax, Order, ItemOrder


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'iso_code')
    search_fields = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'currency')
    list_filter = ('currency',)
    search_fields = ('name',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount_off', 'currency')
    list_filter = ('currency',)


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'percentage',
        'display_name',
        'description',
        'inclusive',
    )
    list_filter = ('inclusive',)


class ItemOrderInline(admin.StackedInline):
    model = ItemOrder
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ItemOrderInline]
    readonly_fields = ('unique_code', 'amount')
    list_display = ('id', 'unique_code', 'tax', 'discount', 'amount')
    list_filter = ('tax', 'discount')
    raw_id_fields = ('items',)


@admin.register(ItemOrder)
class ItemOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'order', 'count')
    list_filter = ('item', 'order')
