from recon import Reconciliation

class ReconciliationReader:
    """Reads all input lines and returns a Reconcillation object that reflects
       - all the Day 0 security balances in the D0-POS section (added)
       - all the security transaction in the D0-TRN section (variouing adds and subtractions)
       - all and Day 1 security balances in the D1-POS section (subracted)
       The reconcile method of the returned Reconciliation object should be called to
       obtain all adjusting entries required to bring security balances to 0
    """
    def read(self, src):
        """Reads lines from source and returns Reconciliation object: see ReconciliationReader doc
             - src: the source of lines
        """
        sections = ('D0-POS', 'D1-TRN', 'D1-POS')
        recon = Reconciliation()
        section = None
        for line in src:
            fields = line.split()
            if not len(fields):
                pass # skip empty/blank lines
            elif fields[0] in sections:
                assert len(fields) == 1
                section = fields[0] # change of section
            elif section == 'D0-POS':
                assert len(fields) == 2
                ( security, shares ) = fields[0:2]
                recon.add(security, shares)
            elif section == 'D1-POS':
                assert len(fields) == 2
                ( security, shares ) = fields[0:2]
                recon.subtract(security, shares)
            elif section == 'D1-TRN':
                assert len(fields) == 4
                ( security, action, shares, cash ) = fields[0:5]
                if security == 'Cash':
                    if action == 'DEPOSIT':
                        recon.add(security, cash)
                    elif action == 'FEE': # or action == 'WITHDRAWAL' ?
                        recon.subtract(security, cash)
                    else :
                        raise "Unknown Cash action: action=" + action
                else:
                    if action == 'BUY':
                        recon.add(security, shares)
                        recon.subtract('Cash', cash)
                    elif action == 'SELL':
                        recon.subtract(security, shares)
                        recon.add('Cash', cash)
                    elif action == 'DIVIDEND':
                        recon.add('Cash', cash)
                    else :
                        raise "Unknown Security action: security=" + security + ", action=" + action
            pass
        return recon
