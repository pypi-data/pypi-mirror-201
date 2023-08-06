# -*- coding: utf-8 -*-
"""
@Time: 2023/3/2 14:38
@Auth: 除以七  ➗7️⃣
@File: setup.py.py
@E-mail: divided.by.07@gmail.com
@Github: https://github.com/divided7
@info: None
"""
import setuptools

setuptools.setup(name='luyuxi',
                 version='0.1.1',
                 description='My personal package',
                 author='divided7',
                 author_email='divided.by.07@gmail.com',
                 packages=setuptools.find_packages(),

                 include_package_data=True,
                 # 列表需要安装的模块，客户端下载时候直接 pip install all_package
                 install_requires=
                    [
                     'tqdm',
                     'opencv-python',
                     'numpy',
                     'matplotlib'
                    ]
                 )
