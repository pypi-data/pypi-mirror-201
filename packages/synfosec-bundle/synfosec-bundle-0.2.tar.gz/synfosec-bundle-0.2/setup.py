from setuptools import setup, find_packages

desc = '''
# RSA GENERATION
'''

setup(
    name='synfosec-bundle',
    description='Lazy RSA generation',
    long_description_content_type='text/markdown',
    long_description=desc,
    author='SYNFOSEC',
    version='0.2',
    packages=find_packages(),
    python_requires='>=3.10',
    install_requires=['pycryptodome'],
    project_urls={
        'Source': 'https://github.com/synfosec/bundle'
    }
)
