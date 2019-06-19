from recon import Reconciliation

class ReconciliationWriter:
    def write(self, recon, dest):
        """Accepts a Reconcillation object and writes adjusting security balance entry 
        lines to the given destination
            - recon: the Reconcillation object (to get adjusting balances entries via the reconcile() method)
            - dest: the destination object
        This writer implementation will write lines in this order:
            - first line is 'Cash' if not zero
            - the remaining lines are written in security symbol order
        """ 
        adjust = recon.reconcile()
        cash = adjust.pop('Cash', None)
        if cash:
            dest.write('Cash' + ' ' + str(cash) + '\n')
        for security in sorted(adjust):
            amount = adjust[security]
            dest.write(security + ' ' + str(amount) + '\n')
