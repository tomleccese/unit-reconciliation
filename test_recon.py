from unittest import TestCase
from recon import Reconciliation
from decimal import Decimal

class ReconciliationTest(TestCase):
    """Customer Account Reconciliation Tests"""

    def setUp(self):
        self.recon = Reconciliation()

    def test_empty(self):
        """test that new/empty Reconcillation object has not security balances"""
        self.assertEqual({}, self.recon.balance)
    
    def test_one_item_non_zero(self):
        """test that reconcile does not return entry for security with zero balance"""
        self.recon.add("WFM", 100)
        self.assertEqual({'WFM': 100}, self.recon.balance)
    
    def test_one_item_non_zero_with_reconcile(self):
        """test that reconcile does return entry for security with non-zero balance"""
        self.recon.add("WFM", 100)
        self.recon.subtract("WFM", 50)
        self.assertEqual({'WFM': -50}, self.recon.reconcile())
    
    def test_sample1(self):
        """test with sample data provided"""
        self.recon.add('GOOG', '200')
        self.recon.add('AAPL', '100')
        self.recon.add('SP500', 175.75)
        self.recon.add('Cash', 1000)

        self.recon.subtract('AAPL', 100)
        self.recon.add('Cash', 30000)
        self.recon.add('GOOG', 10)
        self.recon.subtract('Cash', 10000)
        self.recon.add('Cash', 1000)
        self.recon.subtract('Cash', 50)
        self.recon.add('Cash', 50)
        self.recon.add('TD', 100)
        self.recon.subtract('Cash', 10000)
     
        self.recon.subtract('GOOG', 220)
        self.recon.subtract('SP500', 175.75)
        self.recon.subtract('Cash', 20000)
        self.recon.subtract('MSFT', 10)
        
        actual = self.recon.reconcile()

        expected = {}
        expected['Cash'] = Decimal(8000)
        expected['GOOG'] = Decimal(10)
        expected['TD'] = Decimal(-100)
        expected['MSFT'] = Decimal(10)

        self.assertEqual(expected, actual)
