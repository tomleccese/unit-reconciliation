from recon_reader import ReconciliationReader
from recon_writer import ReconciliationWriter
import sys
from collections import OrderedDict

def main(files):
    """
    Main entry point for doing Reconciliation on one or more input files.
    - files: list of input files (the name '-' can be used to specify sys.stdin)
    * For each input file read the results of the reconciliation is written to a corresponding output file.
    * Any existing content in the output file is overwitten.  
    * The name of the output file is the name of the input file less the trailing '.in' (if it exists) and with a '.out' appended at the end of the name.
    * If the name of an input file is '-' then input is read from sys.stdin and output is written to sys.stdout.
    """
    reader = ReconciliationReader()
    writer = ReconciliationWriter()
    # use OrderedDict to remove duplicate input files in list
    for fname in list(OrderedDict.fromkeys(files)):
        # open file and get Reconciliation from ReconciliationReader
        fin = open(fname) if (fname and not fname == '-') else sys.stdin
        try:
            recon = reader.read(fin)
        finally:
            if not fin == sys.stdin:
                fin.close()
        # write recon to output file
        # output non-stdin to file with same name as input file minus trailing '.in' and with '.out' appended
        fout = open(fname.replace('.in', '') + '.out', 'w') if not (fin == sys.stdin) else sys.stdout
        try:
            writer.write(recon,fout)
        finally:
            if not fout == sys.stdout:
                fout.close()

if __name__ == '__main__':
    main(sys.argv[1:] if len(sys.argv) > 1 else ['-'])
