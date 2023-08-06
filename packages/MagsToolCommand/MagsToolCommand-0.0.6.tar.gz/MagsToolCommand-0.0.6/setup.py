from setuptools import setup, find_packages

setup(
    name='MagsToolCommand',
    version='0.0.6',
    description='Hikesiya',
    author='Hikesiya',
    author_email='hien240891@gmail.com',
    packages=find_packages(),
    package_data={
        '': ['*.txt', '*.h5', '*.pt', '*.py'],
    },
    entry_points={
        'console_scripts': [
            'magstool=MagsToolCommand.run:run'
        ]
    },
    python_requires='>=3.7',
    install_requires=[       
        'click'
    ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
