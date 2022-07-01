from requests import *
from json import *
import unittest


class TestAPIMethods(unittest.TestCase):
    server_ip = 'localhost'
    server_port = 8080

    def test_add(self):
        r = get(f"http://{self.server_ip}:{self.server_port}/add/4/5")
        l = loads(r.text)
        self.assertEqual(l, 9)
        r = get(f"http://{self.server_ip}:{self.server_port}/add/-1/4")
        l = loads(r.text)
        self.assertEqual(l, 3)
        r = get(f"http://{self.server_ip}:{self.server_port}/add/1/-4")
        l = loads(r.text)
        self.assertEqual(l, -3)

    def test_sub(self):
        r = get(f"http://{self.server_ip}:{self.server_port}/sub/5/4")
        l = loads(r.text)
        self.assertEqual(l, 1)
        r = get(f"http://{self.server_ip}:{self.server_port}/sub/-1/4")
        l = loads(r.text)
        self.assertEqual(l, -5)
        r = get(f"http://{self.server_ip}:{self.server_port}/sub/1/-4")
        l = loads(r.text)
        self.assertEqual(l, 5)

    def test_mul(self):
        r = get(f"http://{self.server_ip}:{self.server_port}/mul/4/5")
        l = loads(r.text)
        self.assertEqual(l, 20)
        r = get(f"http://{self.server_ip}:{self.server_port}/mul/-1/4")
        l = loads(r.text)
        self.assertEqual(l, -4)
        r = get(f"http://{self.server_ip}:{self.server_port}/mul/1/-4")
        l = loads(r.text)
        self.assertEqual(l, -4)

    def test_div(self):
        r = get(f"http://{self.server_ip}:{self.server_port}/div/20/5")
        l = loads(r.text)
        self.assertEqual(l, 4)
        r = get(f"http://{self.server_ip}:{self.server_port}/div/23/5")
        l = loads(r.text)
        self.assertEqual(l, 4)
        r = get(f"http://{self.server_ip}:{self.server_port}/div/1/-4")
        l = loads(r.text)
        self.assertEqual(l, -1)
        # doit soulever une exception
        r = get(f"http://{self.server_ip}:{self.server_port}/div/4/0")

    def test_mod(self):
        r = get(f"http://{self.server_ip}:{self.server_port}/mod/20/5")
        l = loads(r.text)
        self.assertEqual(l, 0)
        r = get(f"http://{self.server_ip}:{self.server_port}/mod/23/5")
        l = loads(r.text)
        self.assertEqual(l, 3)
        r = get(f"http://{self.server_ip}:{self.server_port}/mod/1/-4")
        l = loads(r.text)
        self.assertEqual(l, -3)
        # doit soulever une exception
        r = get(f"http://{self.server_ip}:{self.server_port}/mod/4/0")


if __name__ == '__main__':
    unittest.main()
