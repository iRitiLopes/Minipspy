from setuptools import find_packages, setup


setup(
    name="minipspy",
    version="1.0",
    description="Implementation of MIPS architecture",
    author="Richard Lopes",
    author_email="lopes.richard@aluno.ufabc.edu.br",
    packages=find_packages(),
    url="https://ufabc.edu.br",
    py_modules=['main'],
    entry_points="""
        [console_scripts]
        minipspy=main:run
    """
)