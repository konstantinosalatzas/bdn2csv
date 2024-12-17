from setuptools import setup

setup(
    name="bdn2csv",
    version="0.1.0",
    description="SAS BDN XML to CSV converter",
    author="Konstantinos Alatzas",
    url="https://github.com/konstantinosalatzas/bdn2csv",
    packages=[
        'bdn2csv'
    ],
    install_requires=[
        'pandas'
    ]
)
