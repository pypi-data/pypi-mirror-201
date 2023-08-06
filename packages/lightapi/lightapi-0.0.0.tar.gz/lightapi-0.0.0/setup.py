from setuptools import setup, find_packages


setup (
    name = "lightapi",
    # version = "0.0.12",
    author = "Jordan Plows",
    author_email = "jordan@lightapi.com",
    description = "Light AI API turns LLM's into Autonomous Agents",
    readme = "README.rst",
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