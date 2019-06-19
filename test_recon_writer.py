from unittest import TestCase
from decimal import Decimal
from recon_writer import ReconciliationWriter
from io import StringIO
from recon import Reconciliation

class ReconciliationWriterTest(TestCase):

    def setUp(self):
        self.writer = ReconciliationWriter()

    def test_write_empty(self):
        """Assert that the writer writes the expected when there is no lines to write."""
        dest = StringIO()
        try:
            recon = Reconciliation()

            self.writer.write(recon,dest)

            expected = ""
            actual = dest.getvalue()

            self.assertEqual(expected, actual)
        finally:
            dest.close

    def test_write_sample1(self):
        """Assert that the writer writes the given the sample data results as expected."""
        dest = StringIO()
        try:
            recon = Reconciliation()
            recon.add('Cash', -8000)
            recon.add('GOOG', -10)
            recon.add('TD', 100)
            recon.add('MSFT', -10)

            self.writer.write(recon,dest)

            expected = "Cash 8000\nGOOG 10\nMSFT 10\nTD -100\n"
            actual = dest.getvalue()

            self.assertEqual(expected, actual)
        finally:
            dest.close
