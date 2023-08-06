from setuptools import setup, find_packages

setup(
    name='e2e_client',
    version='1.2.6',
    description="This a E2E Client tool for Certbot Plugin",
    author="Abhay Bhati",
    author_email="abhaybhati987@gmail.com",
    packages=find_packages(include=["e2e_client"]),
    install_requires=['requests', 'setuptools', 'whois'],
    include_package_data=True,
)
