from setuptools import setup, find_packages

setup(
    name='multikiwilogger',
    version='1.1.0',
    author='OZRay',
    author_email='d@404.kiwi',
    description='This is a multilogger for LogTail, File and terminal print',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    #url='https://github.com/your-username/my-package',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.0',
    install_requires=[
        'logtail-python'
    ],
)
