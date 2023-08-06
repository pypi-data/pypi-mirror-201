from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder_dz2',
    version='0.0.1',
    author='Kal1m',
    author_email='reznslav@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts':['clean-folder = clean_folder.clean:main']})