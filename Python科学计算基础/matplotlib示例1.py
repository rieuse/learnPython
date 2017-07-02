import matplotlib.pyplot as plt

years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]
GDPs = [256, 289, 302, 356, 389, 400, 402, 436]
plt.plot(years, GDPs, color='green', marker='o', linestyle='solid')
plt.title('小试牛刀')
plt.ylabel('gdp')
plt.show()
