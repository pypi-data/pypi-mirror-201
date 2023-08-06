import setuptools

setuptools.setup(
    name="autosolve-http-client",
    packages=['autosolve_http_client'],
    version="1.0.2",
    author="AYCD Inc",
    author_email="contact@aycd.io",
    description="HTTP Client for connecting to AYCD AutoSolve network",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'urllib3'
    ],
    python_requires='>=3.7',
)
