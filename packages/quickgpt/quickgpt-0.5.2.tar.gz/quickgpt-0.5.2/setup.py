from setuptools import setup, find_packages

setup(
    name='quickgpt',
    version='0.5.2',
    description='A barebones library to make interacting with OpenAI\'s ChatGPT API much simpler.',
    long_description=open("README.rst", "r").read(),
    author='Ben Baptist',
    author_email='me@benbaptist.com',
    url='https://github.com/benbaptist/quickgpt',
    packages=find_packages(),
    scripts=['bin/quickgpt'],
    install_requires=[
        'openai',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
