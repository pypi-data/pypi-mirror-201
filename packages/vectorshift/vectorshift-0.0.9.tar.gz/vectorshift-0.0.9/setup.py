from setuptools import setup, find_packages

VERSION = '0.0.9'
DESCRIPTION = 'A connector to VectorShift'

# Setting up
setup(
    name="vectorshift",
    version=VERSION,
    author="AlexLeonardi",
    author_email="alex.leonardi36@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'vectorshift', 'AI', 'artificial intelligence'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
