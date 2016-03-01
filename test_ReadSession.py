from ReadSession import BookOrder
import unittest

class TestReadSession(unittest.TestCase):
  def test_simple_in_and_out(self):
  	ins = "l9482.5v1V145nb10b09481.0b19480.5b29480.0b39479.5b49479.0b59478.5b69478.0b79477.5b89477.0b99476.5u05u13u21u31u41u52u62u71u811u91na10a09483.5a19484.0a29484.5a39485.0a49485.5a59486.0a69486.5a79487.0a89487.5a99488.0w02w114w22w33w42w54w67w71w86w95"
  	name = "test"
  	timestamp = 12345678
  	bo = BookOrder(name)
  	bo.increment(ins, timestamp)
  	out = bo.toString()
  	print out
