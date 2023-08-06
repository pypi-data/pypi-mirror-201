from setuptools import find_packages, setup


setup(
    name='bs_admin_utils',
    classifiers=[
        'License :: Freely Distributable'
    ],
    packages=find_packages(),
    package_data={
        'bs_admin_utils': ['*.ttf']
    },
    include_package_data=True,
    zip_safe=True,
    version='1.0.0',
    description='Blacksheep admin backend utils classes and function.',
    author='kiki-kanri',
    author_email='a470666@gmail.com',
    keywords=[],
    install_requires=[
        'beanie',
        'blacksheep',
        'kiki_utils',
        'pillow',
        'uvicorn'
    ],
    python_requires=">=3.8"
)
