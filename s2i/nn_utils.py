from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, Dropout
from keras.callbacks import EarlyStopping
from keras.optimizers import SGD
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os


def fit_forecaster(x, y, epochs=100, save_loss=False, base_dir='.'):
    model = Sequential()
    model.add(Conv2D(32, (2, 2), input_shape=x.shape[1:]))
    model.add(Conv2D(32, (2, 2)))
    model.add(Conv2D(32, (2, 2)))
    model.add(Conv2D(32, (3, 3)))
    model.add(Flatten())
    model.add(Dense(128))
    model.add(Dropout(.2))
    model.add(Dense(256))
    model.add(Dense(units=1, activation='sigmoid'))

    opt = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=False)
    model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
    es = EarlyStopping(monitor='val_loss', min_delta=0, patience=10, verbose=1, mode='auto')

    hist = model.fit(x, y, shuffle=True, epochs=epochs, validation_split=0.2, callbacks=[es])
    if save_loss:
        _save_loss(hist, base_dir)

    return model


def _save_loss(data, base_dir):
    plt.plot(data.history['loss'], label='train')
    plt.plot(data.history['val_loss'], label='validation')

    plt.title('Model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend()

    _save_img(os.path.join(base_dir, 'loss.png'))


def save_predictions(test_data, predictions):
    for symbol, data in test_data.symbols_data.items():
        plt.cla()

        # no data before timestep and after -futurestep
        chart = data['ohlcv']['close'].values[test_data.timestep:-test_data.futurestep]
        plt.plot(chart, color='black')

        # gt vs predicted
        y_expected = data['y']
        for idx, (pred, gt) in enumerate(zip(predictions, y_expected)):
            if pred != gt:
                plt.axvspan(idx, idx+1, fc='gray')
                continue
            plt.axvspan(idx, idx+1, fc='green', alpha=.5) if pred else plt.axvspan(idx, idx+1, fc='red', alpha=.5)

        plt.title('Predictions vs Ground Truth - SYMBOL:{}'.format(symbol))
        plt.ylabel('close price')
        plt.xlabel('days')

        legend = [mpatches.Patch(label='positive outlook (gt == pred)', color='green', alpha=.5),
                  mpatches.Patch(label='negative outlook (gt == pred)', color='red', alpha=.5),
                  mpatches.Patch(label='wrong outlook (gt != pred)', color='gray', alpha=.5)]

        plt.legend(handles=legend)

        _save_img('out/{}.png'.format(symbol))


def _save_img(name):
    plt.savefig(name, dpi=300, bbox_inches='tight')
