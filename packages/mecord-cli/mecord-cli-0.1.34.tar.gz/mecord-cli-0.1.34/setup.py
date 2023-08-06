import setuptools

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()
setuptools.setup(
    name="mecord-cli",
    version="0.1.34",
    author="pengjun",
    author_email="mr_lonely@foxmail.com",
    description="mecord tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mecordofficial",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=[],
    # data_files=[
    #     ('widget_template', [
    #         'mecord/widget_template/config.json',
    #         'mecord/widget_template/icon.png',
    #         'mecord/widget_template/index.html'
    #         ]),
    #     ('script_template', [
    #         'mecord/scrip_template/main.py',
    #         'mecord/scrip_template/run.py'
    #         ])
    # ],
    install_requires=[
        'requests',
        'uuid',
        'qrcode',
        'Image',
        'pillow',
        'protobuf',
        'oss2',
        'psutil',
        'qrcode-terminal',
        'pynvml'

    ],
    dependency_links=[],
    entry_points={
        'console_scripts':[
            'mecord = mecord.main:main'
        ]
    },
    # scripts=[
    #     'mecord/upload.py'
    # ],
    python_requires='>=3.4',
)