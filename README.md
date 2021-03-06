# Bloom Term

`bloom-term` is a tool that displays market prices in your terminal. Not quite as nice but a bloomberg terminal, but at least its free!

![bloom-term-demo](./.images/demo.png)

## Dependencies

The only dependendy for `bloom-term` is any `3.x` version of python.

## Usage

- Download `bloom-term.py` locally

```bash
$ git clone https://github.com/nmiodice/bloom-term.git
```

*or*

```bash
$ curl -o bloom-term.py https://raw.githubusercontent.com/nmiodice/bloom-term/master/bloom-term.py
```

- Configure `bloom-term`

```bash
# This controls which symbols bloom-term will query for
export BLOOM_TERM_SYMBOLS="VOO, AMZN, MSFT, DIS, TSLA, VNQ"

# This controls how many symbols will be shown on a line. If this value is missing or set to -1,
# then all results will be printed on a single line.
export BLOOM_TERM_SHOW_PER_LINE="3"

# This controls the HTTP timeout. If it takes longer than this many seconds to complete
# the request, bloom-term will exit without printing anything to the terminal
#
# If this value is missing, bloom-term will default to a 1 second timeout
export BLOOM_TERM_TIMEOUT="0.5"
```

- Run `bloom-term`

```bash
python3 bloom-term.py
```

- Optional: Add to `.bashrc` (or similar)

```bash
# only run for interactive sessions
if [[ $- == *i* ]]; then
    BLOOM_TERM_SYMBOLS="VOO, GOOG, MSFT, DIS, TSLA, VNQ" \
        BLOOM_TERM_SHOW_PER_LINE="3"                     \
        BLOOM_TERM_TIMEOUT="0.5"                         \
        python3 "/path/to/bloom-term.py
fi
```
