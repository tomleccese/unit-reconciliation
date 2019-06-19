from decimal import Decimal

class Reconciliation(object):
    """Customer Account Reconciliation
       - maintains a running balance of security amounts via the add and subtract methods
       - provides the reconcile method to show the adjusting entries required to bring 
          all security balances to zero"""

    def __init__(self):
        self.balance = {}

    def add(self, security, amount):
        """add amount to security"""
        self.balance[security] = self.balance.get(security, Decimal(0)) + Decimal(amount)

    def subtract(self, security, amount):
        """subtract amount from security"""
        self.balance[security] = self.balance.get(security, Decimal(0)) - Decimal(amount)

    def reconcile(self):
        """return a dict with all the entries required to make the balance of all securities equal to 0"""
        diff = {}
        for security, amount in self.balance.items():
            if not amount == Decimal(0):
                diff[security] = -amount
        return diff
