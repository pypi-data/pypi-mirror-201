from __future__ import annotations
import json
from typing import Optional
from sys import getsizeof


def _camelcased(value: str) -> str:
  capitalized = ''.join(x.capitalize() for x in value.split('_'))
  return capitalized[0].lower() + capitalized[1:]


class FabricError(Exception):
  context: Optional[dict[str, str]]
  description: str
  http_code: int = 500
  name: Optional[str]
  return_value: int

  def __init__(
      self,
      context: Optional[dict[str, str]] = None,
      http_code: Optional[int] = None,
      name: Optional[str] = None):
    self.context = context
    if http_code:
      self.http_code = http_code
    self.name = name

  def __iter__(self):
    yield from {
      "context": self.context,
      "name": self.name if self.name else self.__class__.__name__,
      "description": self.description,
      "http_code": self.http_code,
      "return_value": self.return_value
    }.items()

  def __str__(self) -> str:
    return f'''
      {self.__class__.__name__}(name={self.name}, context={self.context}, description={self.description}, \
http_code={self.http_code}, return_value={self.return_value})
    '''

  def __repr__(self) -> str:
    return self.__str__()

  def __sizeof__(self) -> int:
    context_size = getsizeof(self.context) if self.context else 0
    http_code_size = getsizeof(str(self.http_code)) if self.http_code else 0
    return_value_size = getsizeof(str(self.return_value)) if self.return_value else 0

    return context_size \
      + getsizeof(self.description) \
      + http_code_size \
      + getsizeof(self.name) \
      + return_value_size

  def json(self):
    return json.dumps(self, default=lambda o: {_camelcased(k): v for k, v in dict(o).items()}, ensure_ascii=False)
