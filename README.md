# sp500-forecaster
* For a given stock, predict if the mean close price for the next 30 days will be higher/lower than the past 30 days mean close price. 
* Prediction are generated using IEX OHLCV data from the past 144 days.
* The classifier is trained using IEX OHLCV data from S&P500 listed companies.

<p align="center"> 
  <img src="./res/create.gif" alt="margi" width="550" height="375"/>
</p>

## ```create.py```: create+train+evaluate+save forecaster

<details><summary>algorithm details (click to expand)</summary></a>
<p>

1. gather S&P500 OHLCV data and split into train/test
```console
sp500forecaster [DEBUG]: collected 404 train, 101 test sp500 stocks
sp500forecaster [DEBUG]: building train time windows
```

2. transform normalized OHLCV train data into time windows
<img src="./res/create.gif" width="550" height="375" />

3. train forecaster
<img src="./res/train.gif" width="550" height="375" />

4. evaluate on test time windows

<img src="./res/evaluate.gif" width="550" height="375" />

</p>
</details>

<br/>

```console
usage: create.py [-h] [-o OUTPUT] [-v] [-d] stocknum epochs

Create a model to predict future stock trends.

positional arguments:
  stocknum              number of sp500 stocks to retrieve (0=all)
  epochs                number of training epochs

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT,            path to output directory (default ./out)
  -v, --verbose         verbose output, default true
  -d, --debug           visual train info, default false
```

Pretrained weights:

weights | backtest_oa | ```stocknum``` | ```epochs``` | samples
------------- | ------------- | ------------- | ------------- | -------------
[n0_acc0.75_20180918231542.h5](res/n0_acc0.75_20180918231542.h5)  | 0.79 | 0 (all) | 10 | ~259k train, ~65k val, ~85k test

## ```predict.py```: load h5 model weights and predict future prices

```console
usage: predict.py [-h] [-o OUTPUT] [-v] weights symbols [symbols ...]

Predict future stock trends using a pretrained forecaster.

positional arguments:
  weights               path to h5 forecaster weights
  symbols               list of 1 or more iex-supported tickers

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        path to output directory (default ./out)
  -v, --verbose         verbose output, default true

```

Example:
```console
$ python predict.py res/n0_acc0.75_20180918231542.h5 AAPL MMM
Using TensorFlow backend.
sp500forecaster [DEBUG]: symbols: ['AAPL', 'MMM']
sp500forecaster [DEBUG]: processing AAPL
sp500forecaster [DEBUG]: positive future prediction for symbol AAPL
sp500forecaster [DEBUG]: processing MMM
sp500forecaster [DEBUG]: positive future prediction for symbol MMM
```

## Requirements
```console
$ cat /etc/issue*
Ubuntu 16.04.4 LTS
$ python --version
Python 2.7.12
$ pip install -r requirements.txt
...
```
