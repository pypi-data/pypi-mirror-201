from setuptools import setup, find_packages


setup(
    name="misc_utils_aath",
    version="0.1",
    packages=find_packages(),
    install_requires=[
      "PyYAML >= 6.0",
      "icecream >= 2.1",
      "scikit-learn>=1.1.1",
      "umap-learn>=0.5.3",
      "av>=9.2.0",
      "opencv-python>=4.5.5.64"
      "numpy",
      "torch>=1.11.0",
      "pandas>=1.4.2",
      "plotly>=5.8.0"
    ],
    python_requires =">=3.6",
    author="Saandeep Aathreya",

)