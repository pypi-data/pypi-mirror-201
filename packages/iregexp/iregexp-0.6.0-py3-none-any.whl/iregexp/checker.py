"""
IRegexpChecker is appenddown automaton that very quickly determines if a
regular expression using a specified interoperable subset¹ is
syntactically correct.

¹ - https://ietf-wg-jsonpath.github.io/iregexp/draft-ietf-jsonpath-iregexp.html

*/

/* self code is inspired from JSON_checker.c whose license is show hereafter. */

/* 2007-08-24 */

/*
Copyright (c) 2005 JSON.org
Permission is hereby granted, free of charge, to any person obtaining a copy
of self software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and self permission notice shall be included in all
copies or substantial portions of the Software.
The Software shall be used for Good, not Evil.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

from enum import Enum

__ = -1 ## the universal error code

C_NC = 0 ## normal char
C_LPAR = 1 ## (
C_RPAR = 2 ## )
C_QU = 3 ## quantifier
C_CMMA = 4 ## ,
C_RNGE = 5 ## -
C_DOT = 6 ## .
C_DGIT = 7 ## 0-9
C_UA = 8 ## [A-Z] except the following letters...
C_UC = 9 ## C
C_UI = 10 ## I
C_UL = 11 ## L
C_UM = 12 ## M
C_UN = 13 ## N
C_UP = 14 ## P
C_US = 15 ## S
C_UZ = 16 ## Z
C_LBRK = 17 ## [
C_ESC = 18 ## \
C_RBRK = 19 ## ]
C_EXCL = 20 ## ^
C_LA = 21 ## [a-z] except the following letters...
C_LC = 22 ## c
C_LD = 23 ## d
C_LE = 24 ## e
C_LF = 25 ## f
C_LI = 26 ## i
C_LK = 27 ## k
C_LL = 28 ## l
C_LM = 29 ## m
C_LN = 30 ## n
C_LO = 31 ## o
C_LP = 32 ## p
C_LR = 33 ## r
C_LS = 34 ## s
C_LT = 35 ## t
C_LU = 36 ## u
C_LBRC = 37 ## {
C_PIPE = 38 ## |
C_RBRC = 39 ## }


"""
self array maps the 128 ASCII characters into character classes.
The remaining Unicode characters are normal characters C_NC.
"""
ascii_class = [
    C_NC,   C_NC,   C_NC,   C_NC,   C_NC,   C_NC,   C_NC,   C_NC,
    C_NC,   C_NC,   C_NC,   C_NC,   C_NC,   C_NC,   C_NC,   C_NC,
    C_NC,   C_NC,   C_NC,   C_NC,   C_NC,   C_NC,   C_NC,   C_NC,
    C_NC,   C_NC,   C_NC,   C_NC,   C_NC,   C_NC,   C_NC,   C_NC,

    C_NC,   C_NC,   C_NC,   C_NC,   C_NC,   C_NC,   C_NC,   C_NC,
    C_LPAR, C_RPAR, C_QU,   C_QU,   C_CMMA, C_RNGE, C_DOT,  C_NC,
    C_DGIT, C_DGIT, C_DGIT, C_DGIT, C_DGIT, C_DGIT, C_DGIT, C_DGIT,
    C_DGIT, C_DGIT, C_NC,   C_NC,   C_NC,   C_NC,   C_NC,   C_QU, 

    C_NC,   C_UA,   C_UA,   C_UC,   C_UA,   C_UA,   C_UA,   C_UA,
    C_UA,   C_UI,   C_UA,   C_UA,   C_UL,   C_UM,   C_UN,   C_UA,
    C_UP,   C_UA,   C_UA,   C_US,   C_UA,   C_UA,   C_UA,   C_UA,
    C_UA,   C_UA,   C_UZ,   C_LBRK, C_ESC,  C_RBRK, C_EXCL, C_NC,

    C_NC,   C_LA,   C_LA,   C_LC,   C_LD,   C_LE,   C_LF,   C_LA,
    C_LA,   C_LI,   C_LA,   C_LK,   C_LL,   C_LM,   C_LN,   C_LO,
    C_LP,   C_LA,   C_LR,   C_LS,   C_LT,   C_LU,   C_LA,   C_LA,
    C_LA,   C_LA,   C_LA,   C_LBRC, C_PIPE, C_RBRC, C_NC,   C_NC,
]

GO = 0; ##  start
OK = 1 ##  ok
PI = 2 ##  pipe
QM = 3 ##  qty min { requires digit
QN = 4 ##  qty min ... digit or ,
QA = 5 ##  qty max , requires digit
QX = 6 ##  qty max ... digit or }
ES = 7 ##  escape
LB = 8 ##  bracket [ 
BR = 9 ##  bracket [^ ... 
BH = 10 ## bracket [- ... 
BE = 11 ## bracket ... CCE1 or ]
BI = 12 ## bracket ... requires CCchar after ( "-" ccChar )
BJ = 13 ## bracket ... requires CCchar after ( "-" ccChar )
BS = 14 ## bracket \ escape sequence
CP = 15 ## char props \p
CB = 16 ## char props \p{
CE = 17 ## char props \p{·}
PC = 18 ## char props \p{C
PL = 19 ## char props \p{L
PM = 20 ## char props \p{M
PN = 21 ## char props \p{N
PP = 22 ## char props \p{P
PS = 23 ## char props \p{S
PZ = 24 ## char props \p{Z
IS = 25 ## char props \p{I
IT = 26 ## char props \p{Is
IU = 27 ## char props \p{Is·

"""
The state transition table takes the current state and the current symbol,
and returns either a new state or an action. An action is represented as a
negative number. A regular expression is accepted if at the end of the text
the state is OK (or PI) and if the mode is DONE.
"""
state_transition_table = [
## 
##  NC    (    )  *+?    ,    -    .   0-9 A-Z    C    I    L    M    N    P    S    Z    [    \    ]    ^  a-z    c    d    e    f    i    k    l    m    n    o    p    r    s    t    u    {    |    }
  [ -2,  -6,  __,  __,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2, -10,  ES,  __,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  __,  __,  __], ##   /* start       GO */
  [ -2,  -6,  -7,  -3,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2, -10,  ES,  __,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -2,  -4,  -8,  __], ##   /* ok          OK */
  [ -9,  -6,  __,  __,  -9,  -9,  -9,  __,  -9,  -9,  -9,  -9,  -9,  -9,  -9,  -9,  -9, -10,  ES,  __,  -9,  -9,  -9,  -9,  -9,  -9,  -9,  -9,  -9,  -9,  -9,  -9,  -9,  -9,  -9,  -9,  -9,  __,  __,  __], ##   /* pipe        PI */
  [ __,  __,  __,  __,  __,  __,  __,  QN,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __], ##   /* qty min     QM */
  [ __,  __,  __,  __,  QA,  __,  __,  QN,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  -5], ##   /* qty min     QN */
  [ __,  __,  __,  __,  __,  __,  __,  QX,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __], ##   /* qty max     QA */
  [ __,  __,  __,  __,  __,  __,  __,  QX,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  -5], ##   /* qty max     QX */
  [ __,  OK,  OK,  OK,  __,  OK,  OK,  __,  __,  __,  __,  __,  __,  __,  CP,  __,  __,  OK,  OK,  OK,  OK,  __,  __,  __,  __,  __,  __,  __,  __,  __,  OK,  __,  CP,  OK,  OK,  OK,  __,  OK,  OK,  OK], ##   /* escape      ES */
  [ BE,  BE,  BE,  BE,  BE,  BH,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  __,  BS,  __,  BR,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE], ##   /* range       LB */
  [ BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  __,  BS,  __,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE], ##   /* range       BR */
  [ BE,  BE,  BE,  BE,  BE,  __,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  __,  BS, -11,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE], ##   /* range       BH */
  [ BE,  BE,  BE,  BE,  BE,  BI,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  __,  BS, -11,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE], ##   /* range       BE */
  [ BJ,  BJ,  BJ,  BJ,  BJ,  __,  BJ,  BJ,  BJ,  BJ,  BJ,  BJ,  BJ,  BJ,  BJ,  BJ,  BJ,  __,  BS, -11,  BJ,  BJ,  BJ,  BJ,  BJ,  BJ,  BJ,  BJ,  BJ,  BJ,  BJ,  BJ,  BJ,  BJ,  BJ,  BJ,  BJ,  BJ,  BJ,  BJ], ##   /* range       BI */
  [ BE,  BE,  BE,  BE,  BE,  __,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  __,  BS, -11,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE,  BE], ##   /* range       BJ */
  [ __,  BE,  BE,  BE,  __,  BE,  BE,  __,  __,  __,  __,  __,  __,  __,  CP,  __,  __,  BE,  BE,  BE,  BE,  __,  __,  __,  __,  __,  __,  __,  __,  __,  BE,  __,  CP,  BE,  __,  BE,  __,  BE,  BE,  BE], ##   /* range       BS */
  [ __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __, -12,  __,  __], ##   /* char props  CP */
  [ __,  __,  __,  __,  __,  __,  __,  __,  __,  PC,  IS,  PL,  PM,  PN,  PP,  PS,  PZ,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __], ##   /* char props  CB */
  [ __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __, -13], ##   /* char props  CE */
  [ __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  CE,  __,  __,  CE,  __,  __,  __,  __,  CE,  CE,  __,  __,  __,  __,  __,  __,  __, -13], ##   /* char \p{C}  PC */
  [ __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  CE,  CE,  __,  CE,  __,  __,  __,  CE,  CE,  __,  __, -13], ##   /* char \p{L}  PL */
  [ __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  CE,  __,  CE,  __,  __,  __,  __,  __,  CE,  __,  __,  __,  __,  __,  __,  __,  __, -13], ##   /* char \p{M}  PM */
  [ __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  CE,  __,  __,  __,  __,  CE,  __,  __,  CE,  __,  __,  __,  __,  __,  __,  __, -13], ##   /* char \p{N}  PN */
  [ __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  CE,  CE,  CE,  CE,  CE,  __,  __,  __,  __,  CE,  __,  __,  CE,  __,  __,  __,  __, -13], ##   /* char \p{P}  PP */
  [ __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  CE,  __,  __,  __,  __,  CE,  __,  CE,  __,  CE,  __,  __,  __,  __,  __,  __,  __, -13], ##   /* char \p{S}  PS */
  [ __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  CE,  __,  __,  __,  CE,  __,  CE,  __,  __,  __,  __, -13], ##   /* char \p{Z}  PZ */
  [ __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  __,  IT,  __,  __,  __,  __,  __], ##   /* char \p{I}  IS */
  [ __,  __,  __,  __,  __,  IU,  __,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  __,  __,  __,  __,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  __,  __,  __], ##   /* char \p{Is} IT */
  [ __,  __,  __,  __,  __,  IU,  __,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  __,  __,  __,  __,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  IU,  __,  __, -13], ##   /* char \p{Is} IU */
]

## these modes can be appended on the stack
class Mode(Enum):
  DONE = 1
  QUANTITY = 2
  PARENS = 3
  BRACKET = 4
  CPROPS = 5

class IRegexpChecker(object):

  def __init__(self):
    """
    starts the checking process by constructing a new
    IRegexpChecker object.

    To continue the process, call() check for each character
    in the regular expression text, and then call finalCheck()
    to obtain the final result.
    """

    self.state = GO
    self.offset = 0
    self.stack = []
      ## set to True when *, + or ? quantifiers are allowed
    self.quantifiable = False
      ## character classes \p{L} are allowed inside [...]
      ## self boolean is set to True when parsing a character class
      ## inside a [...] range
    self.classExpr = False
    self.append(Mode.DONE)


  def check(self, ch):
    """
    After constructing an IRegexpChecker object, call self
    function for each character (or partial character) in 
    the regular expression.
    It returns if things are looking ok so far.
    If it rejects the text, it throw an error.
    """

    ## print('{} ch: {}, state: {}'.format(self.offset, ch, self.state))

    nextClass = 0
    nextState = 0

    # determine the character's class

    if (ch >= 128):
      nextClass = C_NC
    else:
      nextClass = ascii_class[ch]

    # get the next state from the state transition table

    nextState = state_transition_table[self.state][nextClass]

    ## print('{} ch: {}, next state: {}, next class {}'.format(self.offset, ch, nextState, nextClass))

    if nextState >= 0:
      # change the state
      self.state = nextState

    else:
      # or perform on of the actions
      if nextState == -13: ## \p{ ...}
        self.pop(Mode.CPROPS)
        if self.classExpr:
          self.state = BE
        else:
          self.state = OK
      elif nextState == -12: ## \p{ or \P{
        self.classExpr = self.stack[-1] == Mode.BRACKET
        self.append(Mode.CPROPS)
        self.state = CB
      elif nextState == -11: ## [
        self.pop(Mode.BRACKET)
        self.quantifiable = True
        self.state = OK
      elif nextState == -10: ## [
        self.append(Mode.BRACKET)
        self.state = LB
      elif nextState == -9: ## completed | branch
        self.quantifiable = True
        self.state = OK
      elif nextState == -8: ## |
        self.quantifiable = False
        self.state = PI
      elif nextState == -7: ## )
        self.pop(Mode.PARENS)
        self.quantifiable = True
        self.state = OK
      elif nextState == -6: ## (
        self.append(Mode.PARENS)
        self.quantifiable = False
        self.state = GO
      elif nextState == -5: ## }
        self.pop(Mode.QUANTITY)
        self.state = OK
      elif nextState == -4: ## {
        self.append(Mode.QUANTITY)
        self.state = QM
      elif nextState == -3: ## * + ?
        if not self.quantifiable:
          self.onError()
        self.quantifiable = False
        self.state = OK
      elif nextState == -2: ## atom
        self.quantifiable = True
        self.state = OK
      else:
        self.onError()

      ##print('{} ch: {}, next state: {}'.format(self.offset, ch, nextState))
      self.offset += 1


  def finalCheck(self):
    """
    the finalCheck function shoud be called after all of the characters
    have been processed, but only if every call to check returned
    without throwing an error. self method throws an error if the
    regular expression was not accepted; in other words, the final check failed.
       """

    if not self.state in [OK, PI]:
      self.onError()

    self.pop(Mode.DONE)


  def append(self, mode):
    """
    append a mode onto the stack.
      """
    self.stack.append(mode)
 

  def pop(self, mode):
    """
    pop the stack, ensuring the current mode matches the expectation
    throw and error is the modes mismatch.
    """
    if self.stack.pop() != mode:
      self.onError()

  def onError(self):
    raise Exception('invalid regular expression at character offset {}'.format(self.offset))
