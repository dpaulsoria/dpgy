import numpy as np
import matplotlib.pyplot as plt

# x and y coordinates of the points to fit
x = [1, 2, 3, 4]
y = [2, 4, 1, 5]

# fit a line to the points
coefficients = np.polyfit(x, y, 1)

# create a new figure
plt.figure()

# plot the points
plt.scatter(x, y)

# plot the line of best fit
plt.plot(x, np.polyval(coefficients, x), 'r-')

# add labels and a title to the plot
plt.xlabel('x')
plt.ylabel('y')
plt.title('My Scatter Plot')

# show the plot
plt.show()
