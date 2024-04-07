import unittest

from src.app import Parser


class TestRedisConnection(unittest.TestCase):
    def test_set_command(self):
        parser = Parser()
        values = parser.parse(b"*3\r\n$3\r\nset\r\n$9\r\nraspberry\r\n$5\r\napple\r\n")
        self.assertEqual(values["command"], "ARRAY")
        self.assertEqual(values["args"], ["set", "raspberry", "apple"])

    def test_get_command(self):
        parser = Parser()
        values = parser.parse(b"*2\r\n$3\r\nget\r\n$10\r\nstrawberry\r\n")
        self.assertEqual(values["command"], "ARRAY")
        self.assertEqual(values["args"], ["get", "strawberry"])

    def test_echo_command(self):
        parser = Parser()
        values = parser.parse(b"*2\r\n$4\r\necho\r\n$4\r\npear\r\n")
        self.assertEqual(values["command"], "ARRAY")
        self.assertEqual(list(values["args"]), ["echo", "pear"])

    def test_info_command(self):
        parser = Parser()
        values = parser.parse(b"*1\r\n$4\r\nINFO\r\n")
        self.assertEqual(values["command"], "ARRAY")
        self.assertEqual(list(values["args"]), ["INFO"])

        values = parser.parse(b"*2\r\n$4\r\ninfo\r\n$11\r\nreplication\r\n")
        self.assertEqual(values["command"], "ARRAY")
        self.assertEqual(list(values["args"]), ["info", "replication"])


if __name__ == "__main__":
    unittest.main()
