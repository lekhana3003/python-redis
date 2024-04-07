# Description: Main entry point for the application.
from src.app.redis import Redis
import sys


def main() -> None:

    redis = Redis(args=sys.argv)
    redis.start()


if __name__ == "__main__":
    main()
