from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'An easy way to import your additional packages for Rocket League Python bot development'

# Setting up
setup(
    name="CheeseAgent",
    version=VERSION,
    author="JoshyDev",
    author_email="<iamjoshydev@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'ai', 'development', 'bot building', 'rocket league', 'rlbot'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)