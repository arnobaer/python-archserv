from distutils.core import setup

long_description = open('README.md').read()

setup(
    name="archserv",
    version="0.1.0",
    url="https://github.com/arnobaer/archserv",
    author="Bernhard Arnold",
    author_email="bernhard.arnold@burgried.ch",
    description="",
    long_description=long_description,
    py_modules=["archserv"],
    scripts=["bin/archserv"],
    install_requires=[],
    license="GPLv3",
    keywords="archserv command line parser parsing",
    platforms="any",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ]
)
