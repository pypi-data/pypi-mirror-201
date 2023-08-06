from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cleangpt",
    version="0.1.2",
    author="Emilio Andere",
    author_email="andere.emi@gmail.com",
    description="CLI to make AI-generated text more human-like.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/technoabsurdist/cleangpt",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "aiohttp>=3.8.4",
        "aiosignal>=1.3.1",
        "async-timeout>=4.0.2",
        "numpy>=1.24.2",
        "openai>=0.27.4",
    ],
    entry_points={
        "console_scripts": [
            "your-cli-command=your_package_name.main:cli_entry_point",
        ],
    },
)

