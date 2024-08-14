import matplotlib.pyplot as plt
def plot(rrt_improved, rrt, random_search, floodfill):
    plt.plot(rrt_improved[1], rrt_improved[0], 'r-', label='RRT Improved')
    plt.plot(rrt[1], rrt[0], 'g-', label='RRT')
    plt.plot(random_search[1], random_search[0], 'b-', label='Random Search')
    plt.plot(floodfill[1], floodfill[0], color='black', label='Floodfill')

    ax = plt.gca()
    ax.set_xlim([None, min(rrt[1][-1], rrt_improved[1][-1], random_search[1][-1], floodfill[1][-1])])

    plt.legend(loc="upper left")

    plt.xlabel("Time (s)")
    plt.ylabel("Map Coverage (%)")

    plt.show()