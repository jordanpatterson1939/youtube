import setuptools

with open("README.md","r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="https://github.com/jordanpatterson1939",
    version="0.0.1",
    author="Jordan Patterson",
    author_email="jordanpatterson1939@gmail.com",
    description="Command line tool for converting youtube links to mp3 files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jordanpatterson1939/ytdl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating system :: OS Independent",
    ],
    license='MIT',
    python_requires='>=3.6',
)