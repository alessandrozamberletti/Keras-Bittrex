from datapackage import Package
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def sp500_symbols():
    sp500 = []
    package = Package('https://datahub.io/core/s-and-p-500-companies/datapackage.json')
    for resource in package.resources:
        if resource.descriptor['datahub']['type'] == 'derived/csv':
            sp500 = [s[0].encode('utf-8') for s in resource.read()]

    return sp500


def split(data, ratio):
    split_idx = int(len(data) * ratio)
    return data[:split_idx], data[split_idx:]


def balance(x, y):
    false_y_count = len(y) - np.count_nonzero(np.array(y))
    true_y_idx, = np.where(y)

    np.random.shuffle(true_y_idx)
    x = np.delete(x, true_y_idx[false_y_count:], axis=0)
    y = np.delete(y, true_y_idx[false_y_count:])

    return x, y


def cnn(input_shape):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding="same", input_shape=input_shape))
    model.add(Conv2D(32, (3, 3), padding="same"))
    model.add(Flatten())
    model.add(Dense(64))
    model.add(Dense(64))
    model.add(Dense(units=1, activation='sigmoid'))

    return model


def plot_loss(data):
    plt.figure()
    plt.ion()

    plt.plot(data.history['loss'], label='train')
    plt.plot(data.history['val_loss'], label='validation')

    plt.title('Model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend()

    plt.show()
    plt.pause(0.0001)


def plot_predictions(data, symbols, timestep, futurestep, y_actual, y_expected):
    for symbol in symbols:
        plt.figure()

        symbol_chart = data[symbol]['ohlcv']['close'].values[timestep:]
        plt.plot(symbol_chart, color='black')

        current_avg = np.average(data[symbol]['current'][:, -futurestep:, -1], axis=1)
        plt.plot(current_avg, color='pink')

        future_avg = np.average(data[symbol]['future'][:, :, -1], axis=1)
        plt.plot(future_avg, color='cyan')

        for idx, (y_act, y_exp) in enumerate(zip(y_actual, y_expected)):
            if y_act != y_exp:
                plt.scatter(idx, symbol_chart[idx], marker='+', color='blue')
                continue
            if y_act:
                plt.scatter(idx, future_avg[idx], marker='^', color='green')
            else:
                plt.scatter(idx, current_avg[idx], marker='v', color='red')

        plt.title('Predictions vs Ground Truth - SYMBOL:{}'.format(symbol))
        plt.ylabel('price')
        plt.xlabel('days')

        legend = [Line2D([], [], marker='^', color='green', label='positive outlook', linestyle='None'),
                  Line2D([], [], marker='v', color='red', label='negative outlook', linestyle='None'),
                  Line2D([], [], marker='+', color='blue', label='wrong prediction', linestyle='None'),
                  Line2D([], [], color='pink', label='previous {} days avg. price'.format(futurestep)),
                  Line2D([], [], color='cyan', label='future {} days avg. price'.format(futurestep))]

        plt.legend(handles=legend)

        plt.show()
