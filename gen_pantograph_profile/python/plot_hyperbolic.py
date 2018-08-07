import matplotlib.pyplot as plt
import math

a1 = 2
a2 = 3

x = range(-1200, 1200)
x = [float(ele) / 400 for ele in x]

y1 = [a1 * math.cosh(ele / a1) for ele in x]
y2 = [a2 * math.cosh(ele / a2) for ele in x]

plt.plot(x, y1)
plt.plot(x, y2)

legend_marker = []
legend_marker.append('Larger tension')
legend_marker.append('Smaller tension')
plt.legend(legend_marker, fontsize=16)

plt.title("Hyperbolic function", fontsize=16)
plt.show()
