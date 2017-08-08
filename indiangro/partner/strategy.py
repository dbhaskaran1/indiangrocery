from oscar.apps.partner import strategy
from ipware.ip import get_ip

class Selector(object):

    def strategy(self, request=None, user=None, **kwargs):

        if request is not None:
            return Default(request)


class AllStockRecord(object):
    """
    Stockrecord selection mixin for use with the ``Structured`` base strategy.
    This mixin picks the first (normally only) stockrecord to fulfil a product.

    This is backwards compatible with Oscar<0.6 where only one stockrecord per
    product was permitted.
    """
    def select_stockrecord(self, product):
        try:
            return product.stockrecords.all()[0]
            #if len(product.stockrecords.all())>1:
            #    return product.stockrecords.all()[1]
            #else:
            #    return product.stockrecords.all()[0]
        except IndexError:
            return None


class Default(AllStockRecord, strategy.StockRequired, strategy.NoTax, strategy.Structured):
    """
    stock/price strategy that uses the second found stockrecord for a
    product, ensures that stock is available (unless the product class
    indicates that we don't need to track stock) and charges zero tax.
    """

