from setuptools import setup, find_packages


setup (

    name = "LightAPI",
    version = "0.0.1",
    author = "Jordan Plows",
    author_email = "jordan@lightapi.com",
    url = "https://github.com/light-hq",
    install_requires = [
        "flask",
        "flask-restful",
        "openai",
        "playwright",
        "requests",
        "python-dotenv",
        "flask-cors",
        "Authlib",
    ],
)