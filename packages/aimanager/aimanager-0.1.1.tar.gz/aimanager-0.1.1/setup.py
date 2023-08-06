from setuptools import setup, find_packages

exec(open('aimanager/version.py').read())

setup(
    name='aimanager',
    version=__version__,
    author='Ayoub Assis',
    author_email='assis.ayoub@gmail.com',

    long_description='## scailable-ai-manager-cli',
    long_description_content_type='text/markdown',


    packages=find_packages(),
    python_requires='>=3.8',
    entry_points={
        'console_scripts': ['aimanager=aimanager.cli:cli']
    },
    install_requires=['lgg']
)
