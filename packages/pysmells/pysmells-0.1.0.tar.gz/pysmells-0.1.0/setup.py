from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pysmells",
    version="0.1.0",
    author="Marcos Paulo Alves de Sousa",
    author_email="youremail@example.com",
    description="Uma ferramenta de análise de código Python para verificar a adoção de Type Annotations e relatórios sobre alertas do Pylint e Mypy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pysmells",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='>=3.7',
    install_requires=[
        'tabulate',
        'mypy',
        'pylint',
    ],
    entry_points={
        'console_scripts': [
            'pysmells=pysmells:main',
        ],
    },
)
