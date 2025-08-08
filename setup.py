from setuptools import setup, find_packages

setup(
         name="agentflow",
         version="0.1.0",
         packages=find_packages(),
         install_requires=[
             "typer>=0.9.0",
             "aiohttp>=3.8.0",
             "pyyaml>=6.0.0",
             "beautifulsoup4>=4.12.0",
             "rich>=13.0.0",
         ],
         entry_points={
             "console_scripts": [
                 "agentflow = agentflow.cli:app",
             ],
         },
    )