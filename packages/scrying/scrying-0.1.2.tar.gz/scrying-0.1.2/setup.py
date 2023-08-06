from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent

setup(
    name='scrying',
    version='0.1.2',
    description='A ScryfallAPI port written in Python',
    url='https://github.com/chumpblocckami/scrying',
    author='Matteo Mazzola',
    author_email='contact.matteomazzola@gmail.com',
    license='BSD 2-clause',
    packages=["scrying"],
    install_requires=['requests',
                      'pillow',
                      'tqdm'
                      ],
    long_description=(this_directory / "README.md").read_text(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
