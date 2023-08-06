from setuptools import setup, find_packages


setup(
    name="broker_grpc_lib",
    version="0.3.6",
    description="Python package for easier use message brokers with gRPC application",
    author="multiadmin_optimus_prime",
    author_email="evgenykond@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pydantic>=1.10.4",
        "aio-pika>=9.0.5",
        "grpcio>=1.46.3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
