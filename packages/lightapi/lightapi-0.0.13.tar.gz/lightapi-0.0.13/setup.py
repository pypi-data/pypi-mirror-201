from setuptools import setup
import os
import sys

if sys.version_info[0] < 3:
    with open('README.rst') as f:
        long_description = f.read()
else:
    with open('README.rst', encoding='utf-8') as f:
        long_description = f.read()

# version = {}
# with open(os.path.join('numerov', 'version.py')) as f:
#     exec(f.read(), version)= (this_directory / "README.rst").read_text()

setup (
    name = "lightapi",
    version = "0.0.13",
    author = "Jordan Plows",
    author_email = "jordan@lightapi.com",
    description = "Light API turns LLM's into Autonomous Agents",
    long_description = long_description,
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