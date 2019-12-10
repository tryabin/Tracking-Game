import matplotlib.pyplot as plt
import numpy as np


def main():
    # The file with the scores.
    scoresFileName = './score_history.txt'

    # The number of points that should be plotted.
    numberOfPointsToPlot = 30

    # Ignore scores less than this value.
    minThreshold = 35

    # Get the scores and remove scores that don't meet the minimum threshold.
    scores = np.fromfile(scoresFileName, dtype=np.float64, sep='\n')
    scores = scores[scores > minThreshold]

    # Compute the number of scores that are to be averaged per point.
    binSize = int(len(scores) / numberOfPointsToPlot)


    # Compute the points to plot.
    curSum = 0
    averages = []
    for i in range(len(scores)):

        curSum += scores[i]
        if (i+1) % binSize == 0:
            averages.append(curSum / binSize)
            curSum = 0

            
    # Plot the results.
    plt.figure(figsize=(14, 8))
    plt.plot(averages, 'r-o')
    plt.ylabel('Score')
    plt.show()
    


if __name__ == '__main__':
    main()