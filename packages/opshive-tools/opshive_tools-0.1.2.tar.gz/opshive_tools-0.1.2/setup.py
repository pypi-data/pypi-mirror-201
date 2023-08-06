from setuptools import setup, find_packages

setup(
    name='opshive_tools',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'requests',
        'ansible'
    ],
    entry_points={
        'console_scripts': [
            'my_script = opshive_tools.opshive_tools:main'
        ]
    }
)