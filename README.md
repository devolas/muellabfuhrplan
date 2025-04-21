# Create a Python venv

```
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

```
pip install -r requirements.txt
```

# Program usage

Call the program without arguments to generate all events as full day event (?):
```
python eins.py 
```

If you need a start event bypass the offset and duration, e.g. you want to receive a reminder 6 p.m. the day before, call:

```
python eins.py --offset -6 --duration 1
```

# Run pytests

## Run all tests
Execute from project root:

```
pytest ./tests/
```

## Run a specific test and use print()
```
pytest ./tests/calendar_test.py -s
```