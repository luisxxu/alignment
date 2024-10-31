import argparse
from align import align



def main():
    parser = argparse.ArgumentParser(description="Read Commandline Args")

    parser.add_argument("input", help="Input file")
    parser.add_argument("-m", "--match", type=int, help="Match-score")
    parser.add_argument("-s", "--mismatch", type=int, help="Mismatch-score")
    parser.add_argument("-d", "--indel", type=int, help="Indel")
    parser.add_argument("-a", "--align", help="Include alignment in output", action="store_true")

    args = parser.parse_args()

    filename = args.input
    matchreward = args.match
    mismatchpenalty = args.mismatch
    indelpenalty = args.indel
    outputalignment = args.align
    print(filename)
    printoutput = align(filename, matchreward, mismatchpenalty, indelpenalty, outputalignment)
    print("Score: " + str(printoutput[0]) + "\nLength: " + str(printoutput[1]))

main()