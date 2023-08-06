from iregexp.checker import IRegexpChecker
from iregexp.checker import Mode

__version__ = '0.6.1'

def check(expression):
  """ Checks a given expression is syntactically valid I-Regexp. """
  return checkExpression(expression, True)[0]


def ensureExpression(expression):
  """ Ensures a given expression is syntactically valid I-Regexp. """
  return checkExpression(expression, False)[1]


def toPCRE(expression, anchor = False):
  """
  Ensures a given expression is syntactically valid I-Regexp
  and returns its corresponding PCRE-compatible regex

  Parameters:
    - expression (string): I-Regexp expression
    - anchor (boolean): flag to anchor the resulting expression
  """
  expression = checkExpression(expression, False)[1]
  if anchor:
    return '\\A(?:{})\\Z'.format(expression)
  return expression


def checkExpression(expression, nothrow = True):
  """
  Ensures a given expression is syntactically valid I-Regexp

  Parameters:
    - expression (string): I-Regexp expression to be checked
    - nothrow (boolean): whether to raise an error on failure

  Returns:
    [boolean, string]: if nothrow is set to True, the function
    returns a tuple containing:
    - A boolean True if the given expression is valid I-Regexp
    - A string representing the corresponding PCRE compatible regex

  """

  escape = False
  chars = []

  def peek(inst):
    return inst.stack[-1]

  try:

    checker = IRegexpChecker()
    for ch in expression:
      checker.check(ord(ch))
      ## print('ch: {}({:x}), escape: {}'.format(ch, ord(ch), escape))
      if ord(ch) == 0x2e and (not escape) and peek(checker) != Mode.BRACKET:
        chars += ['[', '^', '\\\\', 'n', '\\\\', 'r', ']']
      else:
        chars.append(ch)
      escape = ord(ch) == 0x5c and (not escape)

    checker.finalCheck()
    return (True, ''.join(chars))

  except Exception as e:
    if nothrow:
      return (False, None)
    else:
      raise e