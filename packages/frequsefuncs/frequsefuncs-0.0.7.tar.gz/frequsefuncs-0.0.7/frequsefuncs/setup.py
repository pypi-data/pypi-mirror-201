

from setuptools import setup, find_packages

VERSION = '0.0.7' 
DESCRIPTION = 'python package of frequently used functions'
LONG_DESCRIPTION = 'python package of frequently used functions'

# Setting up
setup(
       # the name must match the folder name 'frequsefuncs'
        name="frequsefuncs",
        version=VERSION,
        author="y",
        author_email="<y@outlook.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        setup_requires=['wheel'],
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Other Audience",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
        ]

)

