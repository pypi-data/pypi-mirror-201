from setuptools import setup, find_packages

setup(
    name='magstoolnewversion',
    version='0.0.8',
    description='Sample',
    author='MagsTool',
    author_email='hien240891@gmail.com',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'Jinja2==3.1.2',
        'torch==1.13.1',
        'PyYAML==6.0',
        'Pillow==9.4.0',
        'torchvision==0.14.1',
        'numpy==1.21.6',
        'opencv-python==4.7.0.72',
        'matplotlib==3.5.3',
        'pandas==1.3.5',
        'seaborn==0.12.2',
        'requests==2.28.2',
        'tqdm==4.65.0',
        'psutil==5.9.4',
        'thop==0.1.1.post2209072238',
        'tensorflow==2.11.0',
        'XlsxWriter==3.0.9',
        'pdf2image==1.16.3',
        'six==1.16.0',
        'retina-face'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
