#!/usr/bin/env python

import sys
from argparse import ArgumentParser
import numpy as np
import re


def main():
    # usage description
    usage = "Example: ./extractShapes8TeV.py -i InputShapes_RSGqq_PU30_Spring15_M_100.root InputShapes_M_200.root ."

    # input parameters
    parser = ArgumentParser(description='Script extracting resonance shapes from an input ROOT file and printing them in a format used by the interpolation code',epilog=usage)

    parser.add_argument("-i", "--input_filess", dest="input_files", nargs="+", required=True,
                        help="Input files",
                        metavar="INPUT_FILES")

    args = parser.parse_args()

    for input_file in args.input_files:
        print "File " + input_file
        # Get mass from file name
        pattern_mass = re.compile("M_(?P<mass>\d+)")
        match_mass = pattern_mass.search(input_file)
        if match_mass:
            mass = match_mass.group("mass")
        else:
            print "Failed to extract mass from input filename: " + input_file
            sys.exit(1)

        shapes = {}
        binxcenters = []

        # import ROOT stuff
        from ROOT import TFile, TH1F, TH1D
        # open input file
        input_file = TFile(input_file)
        hist = input_file.Get("inclusive/h_pfjet_mjj_over_M")
        bincontents = []

        for i in range(1,hist.GetNbinsX()+1):
            bincontents.append(hist.GetBinContent(i))
            if len(binxcenters) < hist.GetNbinsX():
                binxcenters.append(hist.GetBinCenter(i))

        normbincontents = np.array(bincontents)
        normbincontents = normbincontents/np.sum(normbincontents)

        shapes[mass] = normbincontents.tolist()

        print "shapes = {\n"
        for key, value in sorted(shapes.items()):
            print("  {} : {},".format(key, value))
            print ""
        print "}"
        print ""
        print "binxcenters =", binxcenters
        print ""

if __name__ == '__main__':
    main()
