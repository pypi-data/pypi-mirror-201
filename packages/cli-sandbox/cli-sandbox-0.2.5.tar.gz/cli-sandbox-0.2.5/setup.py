from setuptools import setup, find_packages

setup(
    name='cli-sandbox',
    version='0.2.5',
    description='cli experiments',
    author='Your Name',
    author_email='hughes036@gmail.com',
    url='https://github.com/AllenCell/cli-sandbox',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='your keywords here',
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
    ],
)
