from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='strongmind-powerschool-client',
    version='2.0.4',
    packages=find_packages(),
    url='https://github.com/StrongMind/powerschool-client',
    license='',
    author='team-platform',
    author_email='cinnamon@strongmind.com',
    description='Client for accessing PowerSchool\'s REST API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
)
