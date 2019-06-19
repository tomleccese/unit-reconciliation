from unittest import TestCase
from decimal import Decimal
from recon_reader import ReconciliationReader

class ReconciliationReaderTest(TestCase):
    def setUp(self):
        self.reader = ReconciliationReader()
    
    def test_read_no_input_lines(self):
        """Assert that a reader returns an empty Reconciliation object when there is no input."""
        recon = self.reader.read([])
        self.assertEqual(0, len(recon.balance))

    def test_read_sample1(self):
        """Assert that a reader returns the expected Reconciliation object when given the sample data."""
        lines = []

        lines.append('D0-POS')
        lines.append('AAPL 100')
        lines.append('GOOG 200')
        lines.append('SP500 175.75')
        lines.append('Cash 1000')

        lines.append('D1-TRN')
        lines.append('AAPL SELL 100 30000')
        lines.append('GOOG BUY 10 10000')
        lines.append('Cash DEPOSIT 0 1000')
        lines.append('Cash FEE 0 50')
        lines.append('GOOG DIVIDEND 0 50')
        lines.append('TD BUY 100 10000')
     
        lines.append('D1-POS')
        lines.append('GOOG 220')
        lines.append('SP500 175.75')
        lines.append('Cash 20000')
        lines.append('MSFT 10')
        
        expected = {}
        expected['Cash'] = Decimal(8000)
        expected['GOOG'] = Decimal(10)
        expected['TD'] = Decimal(-100)
        expected['MSFT'] = Decimal(10)

        recon = self.reader.read(lines)

        actual = recon.reconcile()
        self.assertEqual(expected, actual)
