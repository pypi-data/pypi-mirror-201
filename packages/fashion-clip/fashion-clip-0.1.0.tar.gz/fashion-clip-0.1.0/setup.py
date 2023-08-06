from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='fashion-clip',
    version='0.1.0',
    description='',
    author='Jacopo Tagliabue, Patrick John Chia, Federico Bianchi',
    author_email='jtagliabue@coveo.com, pchia@coveo.com, f.bianchi@unibocconi.it',
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=[
        'fashion_clip',
    ],
    classifiers=[
    ],
    install_requires=requirements,
    zip_safe=False
    )