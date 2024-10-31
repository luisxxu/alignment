import os

def align(filename, matchreward, mismatchpenalty, indelpenalty, outputalignment):
    
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



    scorematrix = [[0 for i in range(len(firstseq) + 1)] for j in range(len(secondseq) + 1)]
    maxscore = 0
    maxrow = 0
    maxcol = 0

    for i in range(1, len(firstseq) + 1):
        for j in range(1, len(secondseq) + 1):
            if firstseq[i-1] == secondseq[j-1]:
                match = scorematrix[i-1][j-1] + matchreward
            else:
                match = max(scorematrix[i-1][j-1] - mismatchpenalty, 0)
            insert = scorematrix[i][j-1] - indelpenalty
            deletion = scorematrix[i-1][j] - indelpenalty

            scorematrix[i][j] = max(match, insert, deletion)

            if scorematrix[i][j] >= maxscore:
                maxscore = scorematrix[i][j]
                maxrow = i
                maxcol = j

    firstalign = ""
    secondalign = ""
    blastline = ""
    i = maxrow
    j = maxcol

    while i > 0 and j > 0 and scorematrix[i][j] > 0:
        if scorematrix[i][j] == scorematrix[i-1][j] - indelpenalty:
            firstalign = firstseq[i-1] + firstalign
            secondalign = "-" + secondalign
            blastline = " " + blastline
            i -= 1
        elif scorematrix[i][j] == scorematrix[i][j-1] - indelpenalty:
            firstalign = "-" + firstalign
            secondalign = secondseq[j-1] + secondalign
            blastline = " " + blastline
            j -= 1
        elif scorematrix[i][j] == scorematrix[i-1][j-1] + matchreward:
            firstalign = firstseq[i-1] + firstalign
            secondalign = secondseq[j-1] + secondalign
            if firstseq[i-1] == secondseq[j-1]:
                blastline = "|" + blastline
            else:
                blastline = " " + blastline
            i -= 1
            j -= 1
        else:
            firstalign = firstseq[i-1] + firstalign
            secondalign = secondseq[j-1] + secondalign
            blastline = " " + blastline
            i -= 1
            j -= 1

    if (outputalignment):
        print(firstalign + "\n\n" + secondalign + "\n")
    return maxscore, len(firstalign)
