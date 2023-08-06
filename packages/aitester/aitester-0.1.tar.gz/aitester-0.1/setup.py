from setuptools import setup, find_packages

setup(
    name="aitester",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "click",
        "gitpython",
        "openai",
    ],
    entry_points={
        "console_scripts": [
            "tester=aitest:main",
            'tester-config=aitest.config_manager:manage_config'
        ],
    },
)
