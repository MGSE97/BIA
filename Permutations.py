import datetime
import time

import matplotlib.pyplot as plt

def permute(arr, start=0):
    l = len(arr)

    if start < l:
        for i in range(start, l):
            arr[start], arr[i] = arr[i], arr[start]

            permute(arr, start+1)

            arr[start], arr[i] = arr[i], arr[start]

    elif l < 5:
    #else:
        print(''.join(arr))


def plot_permutations():
    fig = plt.figure('Permutations')
    fig.suptitle('Permutations')
    ax = fig.gca()
    fig.canvas.draw_idle()

    times = []
    ranges = []
    items = (1, 9)
    g, = ax.plot([], [])
    ax.set_xlim(items[0], items[1])

    for c in range(items[0], items[1]+1):
        # Create cities
        cities = list([str(chr(65 + i)) for i in range(0, c)])
        s = time.perf_counter()
        permute(cities)
        e = time.perf_counter()
        times.append(e - s)
        ranges.append(c)
        print('%2d: %s' % (c, datetime.timedelta(seconds=(e-s))))
        g.set_xdata(ranges)
        g.set_ydata(times)
        ax.set_ylim(0, max(times))
        plt.pause(0.1)

    plt.show()