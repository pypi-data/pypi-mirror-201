# I-Regexp Checker

IRegexpChecker is pushdown automaton that very quickly determines if a regular expression using a specified interoperable subset is syntactically correct.

It supports the [I-Regexp](https://ietf-wg-jsonpath.github.io/iregexp/draft-ietf-jsonpath-iregexp.html) specification.

## Install

```sh
pip install iregexp
```

## Usage

```python
from iregexp import check
from iregexp import toPCRE

succeeded = check('[azioyy]*')

## returns PCRE-compatible expression
regex = toPCRE('.*', anchor = True)
```
