from setuptools import setup, find_packages

with open('/home/yaxiong/htmlparsingbs4based/requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='htmlparsingbs4based',
    version='0.0.2',
    author='Yaxiong Yuan',
    author_email='yaxiong.yuan@finquest.com',
    packages=['html_parsing', 'html_parsing.html2text_cp', 'html_parsing.inscriptis_cp', 'utils' ],
    #py_modules=['bacon'],
    url='https://finquest.com/',
    description='This package extracts/parses information from source HTML.',
    long_description=open('README.md', 'r').read(),
    install_requires=requirements,
    python_requires='>=3.8',
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],

    # entry_points={
    #     'console_scripts': [
    #         'htmlparserbs4based = html_parsing.html_parsing_custombs4:parse_single_page',
    #     ]}
)
