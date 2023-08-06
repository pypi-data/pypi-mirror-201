from setuptools import setup, find_packages

setup(
    name='rw_dataframe_data_io',
    version='0.1.4',
    description='A function to read or write data to a file. Supports CSV, JSON, and Pickle file formats.',
    url='https://github.com/dicesare/data_io.git',
    author='antony coco',
    author_email='antony.coco.pro@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.3.0',
        'numpy>=1.23.0',
        'pathlib>=1.0.0',
        'setuptools>=67.6.1',

    ],
    entry_points={
        'console_scripts': [
            'rw-dataframe-data-io=rw_dataframe_data_io.module:fonction'
        ]
    },
    test_suite='tests',
    tests_require=['pytest'],
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)