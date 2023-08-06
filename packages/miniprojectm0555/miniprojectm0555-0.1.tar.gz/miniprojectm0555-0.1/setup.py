from setuptools import setup, find_packages




setup(
    name='miniprojectm0555',
    version='0.1',
    license='MIT',
    author="Maryam Naderi & Lucas Istel",
    author_email='email@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://gitlab.idiap.ch/lstel/m05-naderi-stel',
    keywords='example project',
    install_requires=[
        "numpy",
       "pandas",
       "scikit-learn",
       "setuptools",
       "coverage",
        "furo",

    ],

) 
