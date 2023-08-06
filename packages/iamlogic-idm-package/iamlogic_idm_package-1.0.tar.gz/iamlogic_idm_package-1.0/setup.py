from setuptools import setup, find_packages

setup(
    name='iamlogic_idm_package',
    version='1.0',
    description='IAMLOGIC IDM package',
    author='Prabhu S',
    author_email='info@iamlogic.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'cryptography',
        'sqlalchemy',
        'mysql-connector-python',
        'hvac'       
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

