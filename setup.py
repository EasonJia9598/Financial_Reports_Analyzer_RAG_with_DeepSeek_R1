from setuptools import setup, find_packages

setup(
    name="financial_rag",
    version="0.1.0",
    author="Zesheng Jia",
    author_email="your_email@example.com",
    description="A financial reports analyzer using Retrieval-Augmented Generation (RAG) techniques.",
    long_description_content_type="text/markdown",
    url="https://github.com/EasonJia9598/Financial_Reports_Analyzer_RAG_with_DeepSeek_R1",  # Replace with your actual repository URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "seaborn",
        "scikit-learn",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "financial-rag=financial_rag.main:main",
        ],
    },
)