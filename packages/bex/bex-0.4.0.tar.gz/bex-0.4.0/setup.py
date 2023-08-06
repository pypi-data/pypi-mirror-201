from setuptools import setup, find_packages

setup(
    name="bex",
    version="0.4.0",
    packages=find_packages(),
    install_requires=[
        'tqdm',
        'torch',
        'pandas',
        'numpy',
        'torchvision',
        'h5py',
        'haven-ai',
        'cv2'
    ],
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
    python_requires='>=3.6',
)

