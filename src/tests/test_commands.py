import time
import unittest
import socket


class TestRedisConnection(unittest.TestCase):
    def test_redis_connection(self):
        """
        Test connection to redis server
        """
        try:
            redis_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            redis_socket.connect(("localhost", 6379))
            print("Connected to Redis server successfully.")
        except Exception as e:
            self.fail("Failed to connect to Redis server: {}".format(e))
        finally:
            redis_socket.close()

    def test_ping_command(self):
        """
        Test sending PING command and validating response
        """
        try:
            redis_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            redis_socket.connect(("localhost", 6379))
            redis_socket.send(b"*1\r\n$4\r\nPING\r\n")
            response = redis_socket.recv(1024)
            self.assertEqual(
                response.decode().strip(),
                "+PONG",
                "Invalid response received from Redis server.",
            )
            print("PONG response recieved sucessfully")
        except Exception as e:
            self.fail("Failed running ping command: {}".format(e))
        finally:
            redis_socket.close()

    def test_echo_command(self):
        """
        Test sending echo command and validating response
        """
        try:
            redis_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            redis_socket.connect(("localhost", 6379))
            redis_socket.send(b"*2\r\n$4\r\necho\r\n$4\r\npear\r\n")
            response = redis_socket.recv(1024)
            self.assertEqual(response, b'$4\r\npear\r\n')
            print("echo command response recieved sucessfully")
        except Exception as e:
            self.fail("Failed running echo command: {}".format(e))
        finally:
            redis_socket.close()

    def test_set_command(self):
        """
        Test setting values using set command
        The SET command is used to set a key to a value.
        The tester will expect to receive +OK\r\n as a response
        """
        try:
            redis_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            redis_socket.connect(("localhost", 6379))
            redis_socket.send(b"*3\r\n$3\r\nset\r\n$9\r\nraspberry\r\n$5\r\napple\r\n")
            response = redis_socket.recv(1024)
            self.assertEqual(response.decode().strip(), "+OK")
            redis_socket.send(b"*2\r\n$3\r\nget\r\n$9\r\nraspberry\r\n")
            response = redis_socket.recv(1024)
            self.assertEqual(response, b"$5\r\napple\r\n")
            print("value set sucesfully")
        except Exception as e:
            self.fail("Failed running set command: {}".format(e))
        finally:
            redis_socket.close()
            print("connection closed")

    def test_set_command_with_expiry(self):
        """
        Test setting values using set command
        The SET command is used to set a key to a value.
        The tester will expect to receive +OK\r\n as a response
        """
        try:
            redis_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            redis_socket.connect(("localhost", 6379))
            redis_socket.send(b'*5\r\n$3\r\nset\r\n$6\r\norange\r\n$6\r\nbanana\r\n$2\r\npx\r\n$4\r\n1000\r\n')
            response = redis_socket.recv(1024)
            self.assertEqual(response.decode().strip(), "+OK")
            redis_socket.send(b"*2\r\n$3\r\nget\r\n$6\r\norange\r\n")
            response = redis_socket.recv(1024)
            self.assertEqual(response, b"$6\r\nbanana\r\n")
            time.sleep(2)
            redis_socket.send(b"*2\r\n$3\r\nget\r\n$6\r\norange\r\n")
            response = redis_socket.recv(1024)
            self.assertEqual(response, b"$-1\r\n")

        except Exception as e:
            self.fail("Failed running set command: {}".format(e))
        finally:
            redis_socket.close()
            print("connection closed")

    def test_get_command(self):
        """
        get command is for getting values set using set command
        The GET command is used to get the value for the provided key.
        The tester will expect to receive $<len value>\r\n<value>\r\n
        """
        try:
            redis_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            redis_socket.connect(("localhost", 6379))
            redis_socket.send(b"*2\r\n$3\r\nget\r\n$10\r\nstrawberry\r\n")
            response = redis_socket.recv(1024)
            self.assertEqual(response, b"$-1\r\n")
            print("value returned sucessfully")
        except Exception as e:
            self.fail("Failed running set command: {}".format(e))
        finally:
            redis_socket.close()
            print("connection closed")

    def test_info_command(self):
        """
        get command is for getting values set using set command
        The GET command is used to get the value for the provided key.
        The tester will expect to receive $<len value>\r\n<value>\r\n
        """
        try:
            redis_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            redis_socket.connect(("localhost", 6379))
            redis_socket.send(b"*1\r\n$4\r\nINFO\r\n")
            response = redis_socket.recv(1024)
            self.assertEqual(response, b"$11\r\nrole:master\r\n")
            print("value returned sucessfully")
        except Exception as e:
            self.fail("Failed running set command: {}".format(e))
        finally:
            redis_socket.close()
            print("connection closed")
    def test_psync_command(self):
        """
        get command is for getting values set using set command
        The GET command is used to get the value for the provided key.
        The tester will expect to receive $<len value>\r\n<value>\r\n
        """
        try:
            redis_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            redis_socket.connect(("localhost", 6379))
            redis_socket.send(b"*3\r\n$5\r\nPSYNC\r\n$1\r\n?\r\n$2\r\n-1\r\n")
            response = redis_socket.recv(1024)
            self.assertEqual(response, b'+FULLRESYNC 8371b4fb1155b71f4a04d3e1bc3e18c4a990aeeb 0\r\n')
            response = redis_socket.recv(1024)
            print(response)
            print("value returned sucessfully")
        except Exception as e:
            self.fail("Failed running set command: {}".format(e))
        finally:
            redis_socket.close()
            print("connection closed")


if __name__ == "__main__":
    unittest.main()
