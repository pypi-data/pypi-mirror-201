from setuptools import setup, find_packages


setup(
    name="qrcode-cli",
    version="0.1.0",
    url="",
    author="Lapis Pheonix",
    description="A command-line interface for generating QR codes",
    packages=find_packages(),
    install_requires=["qrcode==7.4.2"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
