from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='html_for_nlp',
    version='0.0.1',
    author='Róbert Druska',
    author_email='robert.druska@gmail.com',
    description='HTML for NLP',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/druskacik/html_for_nlp',
    license='MIT',
    packages=['html_for_nlp'],
    install_requires=[
        'beautifulsoup4',
        'lxml',
    ],
)