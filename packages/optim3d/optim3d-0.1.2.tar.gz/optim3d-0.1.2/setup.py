from setuptools import setup, find_packages

setup(
    name="optim3d",
    version='0.1.2',
    description="CLI application for efficient and optimized reconstruction of large-scale 3D building models",
    author = 'Anass Yarroudh',
    author_email = 'ayarroudh@uliege.be',
    url = 'https://github.com/Yarroudh/Optim3D',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "optim3d=optim3d.main:cli"
        ]
    }
)
