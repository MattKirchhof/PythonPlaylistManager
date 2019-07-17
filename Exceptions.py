class NotFoundException(RuntimeError):
   def __init__(self, code):
      self.code = code

class LastFMException(Exception):
   def __init__(self, code):
      self.code = code

class GenericConnectionException(Exception):
   def __init__(self, code):
      self.code = code
