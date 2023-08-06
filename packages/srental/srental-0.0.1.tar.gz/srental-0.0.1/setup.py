from setuptools import setup, find_packages

setup(
    name='srental',
    version='0.0.1',
    author='MingXing Xiao',
    author_email='xiaomixin@gmail.com',
    description='Used to optimize the profitability of a small rental company with a single spaceship to rent.',
    include_package_data=True,
    packages=find_packages(),
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=[
        'flask==2.2.3',
        'python-dotenv==1.0.0',
    ],
)
