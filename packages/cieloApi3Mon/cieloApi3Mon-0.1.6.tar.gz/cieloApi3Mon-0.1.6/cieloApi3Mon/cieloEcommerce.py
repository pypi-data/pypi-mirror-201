from .request.createSale import CreateSale
from .request.querySale import QuerySale
from .request.updateSale import UpdateSale
from .request.createCardToken import CreateCardToken
from .request.queryRecorrency import QueryRecorrency
from .request.deactivateRecorrency import DeactivateRecorrency
from .request.reactivateRecorrency import ReactivateRecorrency


class CieloEcommerce(object):
    def __init__(self, merchant, environment):
        self.environment = environment
        self.merchant = merchant
        self.request = None

    def create_sale(self, sale):
        self.request = CreateSale(self.merchant, self.environment)

        return self.request.execute(sale)

    def capture_sale(self, payment_id, amount=None, service_tax_amount=None):
        self.request = UpdateSale('capture', self.merchant, self.environment)

        self.request.amount = amount
        self.request.service_tax_amount = service_tax_amount

        return self.request.execute(payment_id)

    def cancel_sale(self, payment_id, amount=None):
        self.request = UpdateSale('void', self.merchant, self.environment)

        self.request.amount = amount

        return self.request.execute(payment_id)

    def get_sale(self, payment_id):
        self.request = QuerySale(self.merchant, self.environment)

        return self.request.execute(payment_id)

    def create_card_token(self, creditCard):
        self.request = CreateCardToken(self.merchant, self.environment)

        return self.request.execute(creditCard)

    def get_recurrent_payment(self, recurrent_payment_id):
        self.request = QueryRecorrency(self.merchant, self.environment)

        return self.request.execute(recurrent_payment_id)

    def deactivate_recurrent_payment(self, recurrent_payment_id):
        self.request = DeactivateRecorrency(self.merchant, self.environment)

        return self.request.execute(recurrent_payment_id)

    def reactivate_recurrent_payment(self, recurrent_payment_id):
        self.request = ReactivateRecorrency(self.merchant, self.environment)

        return self.request.execute(recurrent_payment_id)

    def get_last_request(self, print_out=False):
        return self.request.get_last_request(print_out)
