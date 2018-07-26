import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader as web
from datapackage import Package
import random

# TODO: check how to speed it up, avoid locking for too long
print 'Collecting SP500 stocks..'
package = Package('https://datahub.io/core/s-and-p-500-companies/datapackage.json')
for resource in package.resources:
    if resource.descriptor['datahub']['type'] == 'derived/csv':
        sp500 = [s[0].encode('utf-8') for s in resource.read()]

stocks = random.sample(sp500, 1)
print('Retrieving data for: {}'.format(', '.join(stocks)))
timestep = 144
data = web.DataReader(stocks, data_source='morningstar')

# TODO: check if the samples with their relative gt are correctly computed
# TODO: plot data window + gt for random stocks
print('Splitting into time samples..')
debug = True
X = []
y = []

future_window = 30
import matplotlib.pyplot as plt
plt.ion()
for stock in stocks:
    ohlc = data.xs(stock).values
    for t in range(0, ohlc.shape[0] - timestep - future_window):
        current = ohlc[t:t + timestep, 1:4]
        future = ohlc[t + timestep - 1:t + timestep - 1 + future_window, 3]

        future_avg_price = np.average(future)
        current_avg_price = np.average(current[:, -1])
        trend = future_avg_price > current_avg_price

        p0 = current[0, :]
        current = [[(i[0]/p0[0])-1, (i[1]/p0[1])-1, (i[2]/p0[2])-1] for i in current]
        future = [(i/p0[-1])-1 for i in future]
        current = np.array(current)
        future = np.array(future)
        X.append(current.reshape(12, 12, 3))
        y.append(trend)

        if debug:
            plt.cla()
            plt.plot(current[:, -1],
                     color='black')
            plt.plot([(current_avg_price/p0[-1])-1 for i in range(len(current))],
                     color='gray',
                     label='current avg price')

            xi = [i for i in range(timestep - 1, timestep - 1 + future_window)]
            color = 'green' if trend else 'red'
            plt.plot(xi,
                     future,
                     linestyle='--',
                     color='gray')
            plt.plot(xi,
                     [(future_avg_price/p0[-1])-1 for i in range(len(xi))],
                     color=color,
                     label='future avg price')

            plt.title('Sample [{0}]'.format(stock))
            plt.xlabel('days')
            plt.ylabel('normalized closing price')
            plt.legend(loc='upper left')
            plt.show()
            plt.pause(.1)

print('{} time windows collected'.format(len(X)))

exit(0)

# TODO: balance dataset, #downtrend windows = #uptrend windows
X = np.array(X)
y = np.array(y)
false_count = len(y) - np.count_nonzero(y)
true_idx, = np.where(y)

model = Sequential()
model.add(Conv2D(20, (3, 3), padding="same", input_shape=(12, 12, 3)))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Conv2D(20, (3, 3), padding="same"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Flatten())
model.add(Dense(128))
model.add(Dense(units=1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, y, shuffle=True, epochs=100, validation_split=0.33)

# TODO: plot test data windows + classification vs expectation for random stocks
