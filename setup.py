from setuptools import setup, find_packages

setup(
    name='py_context_logger',
    version='1.0.4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    license='MIT',
    description='A context custom logger with thread-local storage and context propagation for Python applications.',
    long_description=open('README.MD').read(),
    long_description_content_type='text/markdown',
    url='',
    author='Rajesh Ganjikunta',
    author_email='rajeshkumarganjikunta90@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
