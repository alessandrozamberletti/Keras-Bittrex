# stock2image

For any stock, given hlc data from the past 144 days, predict if the average closing price in the next 30 days will be
higher or lower than today's closing price.

## Pipeline
* Instead of using rnn/lstm, we transform 144 days of hlc data to a (12,12,3) image and feed it to a cnn.
* stock2image
* img -> train samples pipeline
* model train
* img -> accuracy
* model eval
* img -> gt vs pred

* tested on ubuntu 16.04, python 2.7
```
pip install -r requirements.txt
```
