from setuptools import setup, find_packages


setup(
    name='exergenics',
    version='2.4.0',
    author="John Christian",
    author_email='john.christian@exergenics.com',
    packages=['exergenics'],
    long_description="",
    long_description_content_type="text/markdown",
    # package_dir={'': 'src'},
    url='https://github.com/Exergenics/internal-portal-api',
    keywords='exergenics portal api',
    install_requires=[
        'boto3',
        'datetime',
        'requests',
        'urllib3',
        'logtail-python'
    ],
    extras_require={
        "dev": ["pytest >= 7.0", "twine >= 4.0.2", "bump == 1.3.2"],
    },
    python_requires=">=3.8.10"
)
