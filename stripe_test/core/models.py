from django.db import models


class Currency(models.Model):
    
    name: str = models.CharField(verbose_name='Название валюты', max_length=64)
    iso_code: str = models.CharField(verbose_name='ISO', max_length=3, blank=True, null=True, default='usd')
    
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'


class Item(models.Model):
    
    name: str = models.CharField(verbose_name='Название товара', max_length=128)
    description: str = models.CharField(verbose_name='Описание товара', max_length=256)
    price: float = models.PositiveIntegerField(verbose_name='Стоимость')
    currency: Currency = models.ForeignKey(Currency, verbose_name='Валюта', on_delete=models.SET_DEFAULT, default=1)
    
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        default_related_name = '%(class)ss'


class Discount(models.Model):
    
    amount_off: int = models.IntegerField(verbose_name='Размер скидки')
    currency: Currency = models.ForeignKey(Currency, verbose_name='Валюта', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.amount_off} {self.currency}'

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'
    
    @property
    def json(self):
        return {
            'amount_off': self.amount_off * 100,
            'currency': self.currency.iso_code,
        }


class Tax(models.Model):
    
    percentage: int = models.IntegerField(verbose_name='Размер налога')
    display_name: str = models.CharField(verbose_name='Аббривиатура налога', max_length=16, default='VAT')
    description: str = models.CharField(verbose_name='Описание налога', max_length=16, default='VAT')
    inclusive: bool = models.BooleanField(verbose_name='Включен?', default=True)

    def __str__(self):
        return f'{self.percentage}%'

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'
    
    @property
    def json(self):
        return {
            'percentage': self.percentage,
            'display_name': self.display_name,
            'description': self.description,
            'inclusive': self.inclusive,
        }


class Order(models.Model):

    unique_code: str = models.CharField(verbose_name='Уникальный код заказа', null=True, blank=True, max_length=32)
    items = models.ManyToManyField(to=Item, through='itemorder', verbose_name='Товары')
    tax: Tax = models.ForeignKey(Tax, verbose_name='Размер налога', on_delete=models.SET_NULL, null=True, blank=True)
    discount: Discount = models.ForeignKey(Discount, verbose_name='Размер скидки', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Заказ {self.pk}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class ItemOrder(models.Model):
    
    item: Item = models.ForeignKey(Item, verbose_name='Товар', on_delete=models.CASCADE)
    order: Order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE)
    count: int = models.PositiveIntegerField(verbose_name='Количество товара в заказе')
    
    def __str__(self):
        return f'{self.item.name} в заказе {self.order.pk}'

    class Meta:
        verbose_name = 'Товар к заказу'
        verbose_name_plural = 'Товары к заказам'
        default_related_name = '%(class)ss'
