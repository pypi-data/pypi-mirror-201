from setuptools import setup, find_packages


setup(
    name='flashquiz',
    version="0.5",
    description='Practice your flashcards using python',
    author='mike-fmh',
    author_email='mikemh@uri.edu',
    license='MIT',
    packages=find_packages(),
    package_data={
        'flashquiz': ['default.csv', 'assets/*']
    },
    entry_points={'console_scripts': ['flashquiz = flashquiz.quizzer:main']},
    install_requires=[
        'pygame',
        'argparse'
    ]
)
