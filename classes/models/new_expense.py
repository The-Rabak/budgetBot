from budgetBot.classes.models.model import Model
from budgetBot.classes.singleton import Singleton

class NewExpense(Model, metaclass=Singleton):
    def __init__(self, user = '', business_name = '', product = '', amount = 1, payments = 1, method = ''):
        super().__init__()
        self.business_name = business_name
        self.product = product
        self.amount = amount
        self.payments = payments
        self.payment_method = method
        self.user = user

    
    def set_amount(self, amount):
        self.amount = amount
    
    def set_user(self, user):
        self.user = user
    def set_payments(self, payments):
        self.payments = payments
    def set_product(self, product):
        self.product = product
    def set_payment_method(self, payment_method):
        self.payment_method = payment_method
    def set_business_name(self, business_name):
        self.business_name = business_name   

    def set_default_values(self):
        self.set_amount(0)
        self.set_payments(0)
        self.set_product('')
        self.set_payment_method('')
        self.set_business_name('')

    def to_dict(self, reset = False):
        dict_values =  {
                "business_name": self.business_name,
                "payment_method": self.payment_method,
                "product": self.product,
                "payments": self.payments,
                "amount": self.amount,
                "user": self.user,
                }  
        if reset:   
            self.set_default_values()
        return dict_values