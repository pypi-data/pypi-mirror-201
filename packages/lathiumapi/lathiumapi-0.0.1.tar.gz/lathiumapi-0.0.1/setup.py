from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Python Discord Libary for the API of Lathium Tool!'
LONG_DESCRIPTION = 'The Official Package for Manage our API only for you!'

# Setting up
setup(
    name="lathiumapi",
    version=VERSION,
    author="RequiredHandler",
    author_email="noemail@nomail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python', 'pyautogui', 'pyaudio'],
    keywords=['python', 'lathium', 'lathiumtool', 'lathiumsystem', 'lathiumapi', 'lathiumdiscord'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)