from client.web_interface import WebApp
import os


def main():
    app = WebApp(os.environ.get("GROQ_API_KEY"))


if __name__ == '__main__':
    main()
