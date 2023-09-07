class Dummy:
  def __init__(self, title=''):
    pass
  def __getattr__(self, name):
    return self.dummy
  def dummy(self, *args):
    pass
