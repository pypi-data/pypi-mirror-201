from setuptools import setup, find_packages


setup(
    name="ExpdFtpService",
    version="0.5.0",
    license='MIT',
    author="greg he",
    author_email='greg.he@expeditors.com',
    description="Python Module for download / upload file on Expeditors Ftp Server",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='download / upload ftp file',
    install_requires=[
        'loguru'
    ],
)