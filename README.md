

<h3 align="center">Python Redis: A reimplementation of redis in pure python</h3>

<p align="center">

[//]: # (<a href="https://github.com/laixintao/iredis/actions"><img src="https://github.com/laixintao/iredis/workflows/Test/badge.svg" alt="Github Action"></a>)

[//]: # (<a href="https://badge.fury.io/py/iredis"><img src="https://badge.fury.io/py/iredis.svg" alt="PyPI version"></a>)
   
[//]: # (<a href="https://pepy.tech/project/iredis"><img src="https://pepy.tech/badge/iredis" alt="Download stats"></a>)
</p>
<p align="center">
      <img src="https://badgen.net/badge/python/3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11" alt="Python version">
   
</p>
<p align="center">
    <img src="./resources/demo.gif" alt="demo">
</p>
<p align="center">
    <a href="#features">Features</a> •
    <a href="#how-to-use">How to Use</a> •
    <a href="#contributing">Contributing</a> •
    <a href="#license">License</a> •
    <a href="#contact">Contact</a>
</p>

# Python-Redis

Python-Redis is a Python reimplementation of Redis, a popular in-memory data structure store used as a database, cache. Python-Redis aims to provide similar functionality to Redis while being written entirely in Python, making it easier to understand, modify, and extend.

## Features

- **Commands**: Python-Redis supports currently support all basic commands, allowing users to store and retrieve data efficiently.

- **Redis Client Compatibility**: Python-Redis can be connected to using any Redis client that supports the Redis protocol. This ensures compatibility with existing Redis clients and libraries.

## How to Use

To start using Python-Redis, follow these simple steps:

1. Clone the repository:
   ```
   git clone https://github.com/lekhana3003/python-redis.git
   ```

2. Navigate to the project directory:
   ```
   cd python-redis
   ```

3. Run the Python-Redis server:
   ```
   ./spawn-redis-server.sh --port <port>
   ```

4. Connect to Python-Redis using a Redis client of your choice, specifying the host and port where Python-Redis is running.

Note: Used [iredis](https://github.com/laixintao/iredis) for demo 

## Contributing

Contributions are welcome! If you'd like to contribute to Python-Redis, please follow these guidelines:

- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes.
- Write tests for your changes.
- Ensure all tests pass.
- Submit a pull request.

## License

Python-Redis is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions, suggestions, or issues, please feel free to contact me at [lekhanag.3003@gmail.com](mailto:lekhanag.3003@gmail.com).

---

Python-Redis is a project by [Lekhana Ganji](https://github.com/lekhana3003).
