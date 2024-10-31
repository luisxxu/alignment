import os
import argparse
from align import align



def main():
    parser = argparse.ArgumentParser(description="Read Commandline Args")

    parser.add_argument("input", help="Input file")
    parser.add_argument("-m", "--match", type=int, help="Match-score")
    parser.add_argument("-s", "--mismatch", type=int, help="Mismatch-score")
    parser.add_argument("-d", "--indel", type=int, help="Indel")

    args = parser.parse_args()

    filename = args.input
    matchreward = args.match
    mismatchpenalty = args.mismatch
    indelpenalty = args.indel
    curralign = align(filename, matchreward, mismatchpenalty, indelpenalty, -1, -1)
    back = backtrace(curralign[0], curralign[1], curralign[2], curralign[3], curralign[4], curralign[5], curralign[6], matchreward, mismatchpenalty, indelpenalty, filename)
    print("Score: " + str(back[0]) + "\nLength: " + str(back[1]))

def align(filename, matchreward, mismatchpenalty, indelpenalty, firstlength, secondlength):
    
    firstseq = ""
    secondseq = ""

    with open(os.getcwd() + "/" + filename, "r") as inputfile:
        filecontent = inputfile.readlines()
        start = 0
        for line in filecontent:
            line = line.strip()
            if line.startswith(">"):
                start += 1
            elif start == 1 and len(line) > 0:
                firstseq = line
            elif start == 2 and len(line) > 0:
                secondseq = line

    if (firstlength != -1 and secondlength != -1):
        maxlength = max(firstlength, secondlength)
        firstseq = firstseq[0:firstlength]
        secondseq = secondseq[0:secondlength]
        firstlength += 1
        secondlength +=1
    else:
        firstlength = len(firstseq) + 1
        secondlength = len(secondseq) + 1

    prevrow = [0] * (secondlength)
    maxscore = 0
    maxrow = 0
    maxcol = 0

    for i in range(1, len(firstseq) + 1):
        currrow = [0] * (secondlength)
        for j in range(1, len(secondseq) + 1):
            if firstseq[i-1] == secondseq[j-1]:
                match = prevrow[j-1] + matchreward
            else:
                match = max(prevrow[j-1] - mismatchpenalty, 0)
            insert = currrow[j-1] - indelpenalty
            deletion = prevrow[j] - indelpenalty

            currrow[j] = max(match, insert, deletion)
                    

            if currrow[j] >= maxscore:
                maxscore = currrow[j]
                maxrow = i
                maxcol = j

        if (i != len(firstseq)):
            prevrow = currrow

    return (prevrow, currrow, maxrow, maxcol, firstseq, secondseq, maxscore)

def backtrace(prevrow, currrow, maxrow, maxcol, firstseq, secondseq, maxscore, matchreward, mismatchpenalty, indelpenalty, filename):
    firstalign = ""
    secondalign = ""
    score = 0
    i = maxrow
    j = maxcol
    print(i)
    print(j)

    newalign = align(filename, matchreward, mismatchpenalty, indelpenalty, i, j)
    prevrow = newalign[0]
    currrow = newalign[1]
    readjust = 0

    while maxscore != score and i >= 0 and j >= 0:
        if currrow[j] == prevrow[j] - indelpenalty:
            score -= indelpenalty
            firstalign = firstseq[i-1] + firstalign
            secondalign = "-" + secondalign
            i -= 1
            readjust = 1
        elif currrow[j] == currrow[j-1] - indelpenalty:
            score -= indelpenalty
            firstalign = "-" + firstalign
            secondalign = secondseq[j-1] + secondalign
            j -= 1
            readjust = 0
        elif currrow[j] == prevrow[j-1] + matchreward:
            score += matchreward
            firstalign = firstseq[i-1] + firstalign
            secondalign = secondseq[j-1] + secondalign
            i -= 1
            j -= 1
            readjust = 1
        else:
            score -= mismatchpenalty
            firstalign = firstseq[i-1] + firstalign
            secondalign = secondseq[j-1] + secondalign
            i -= 1
            j -= 1
            readjust = 1
        if (readjust == 1 and i > 0 and j > 0):
            newalign = align(filename, matchreward, mismatchpenalty, indelpenalty, i, j)
            prevrow = newalign[0]
            currrow = newalign[1]
            readjust = 0
    print(firstalign + "\n\n" + secondalign + "\n")
    return (score, len(firstalign))
main()