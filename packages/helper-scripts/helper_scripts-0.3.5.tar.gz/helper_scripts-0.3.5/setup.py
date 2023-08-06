from setuptools import setup, find_packages
setup(
    name = 'helper_scripts',
    packages = ['database_handler','send_mail'],
    version='0.3.5',
    author='Samuel Kizza',
    author_email='samuel.kizza@finca.org',
    description='Database helper package',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
    "psycopg2",
    "pandas",
    "petl"
    ]
    # requires=[
    #     'psycopg2',
    #     'pandas'
    # ],
)