from setuptools import find_packages, setup

setup(
    name="dotm",
    version="0.0.1",
    url="https://github.com/winpat/dotm",
    author="Patrick Winter",
    author_email="patrickwinter@posteo.ch",
    description="A symlink-based dotfile manager with support for multiple hosts",
    packages=find_packages(),
    install_requires=[
        "PyYAML >= 5.2",
    ],
    entry_points={"console_scripts": ["dotm = dotm.main:main"]},
)
