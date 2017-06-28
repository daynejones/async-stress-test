A way to stress test a tracking pixel using the new and shiny async features of Python 3.5

Usage

1. Start a new virtual environment

```
virtualenv .
```

1. Use python 3

```
virtualenv -p $(which python3) .
```

1. Run the script

```
python3 -W ignore stress-test-pixel.py <URL> <delay>
```
