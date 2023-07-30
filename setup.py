from setuptools import setup, find_packages
from pathlib import Path

base_path = Path(__file__).parent
long_description = (base_path / "README.md").read_text()


setup(
    name="aioclaude-api",
    version="1.0.15",
    author="Hikamoru",
    license="MIT",
    author_email="me.thefarkhodov@gmail.com",
    description="An unofficial API for Claude AI, allowing users to access and interact with Claude AII",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AmoreForever/Claude-API/",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    package_dir={"": "aioclaude-api"},
    py_modules=["aioclaude_api", "claude_api"],
    keywords=[
        "claude",
        "ai",
        "claude-ai",
        "API",
        "requests",
        "chatbot",
        "async",
        "aiohttp",
    ],
    install_requires=[
        "aiohttp",
        "requests",
    ],
    python_requires=">=3.8",
)
