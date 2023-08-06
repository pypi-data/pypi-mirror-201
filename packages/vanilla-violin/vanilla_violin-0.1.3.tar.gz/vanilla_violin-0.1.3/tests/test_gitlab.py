from vanilla_violin import Gitlab
from ddt import ddt, data, unpack

import unittest

@ddt
class TestFindGroupByPath(unittest.TestCase):

  GROUPS = [
    {
      "id":56789,
      "path":"badjumbas"
    },
    {
      "id":12345,
      "path":"massusso"
    },
    {
      "id":11111,
      "path":"alioli"
    }
  ]

  @data(('massusso', {'id': 12345, 'path': 'massusso'}), ('nao-existo-lel', []))
  @unpack
  def test_group_found(self, value, expectation):
    gitlab = Gitlab('')
    group = gitlab.find_object_by_path(value, self.GROUPS)
    self.assertEqual(group, expectation)