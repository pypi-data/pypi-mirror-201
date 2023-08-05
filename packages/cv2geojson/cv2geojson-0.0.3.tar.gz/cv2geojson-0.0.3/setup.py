from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'Export contour annotations as geojson formatted data'

# Setting up
setup(
    name="cv2geojson",
    version=VERSION,
    author="Mohsen Farzi",
    author_email="<mhnfarzi@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python', 'numpy', 'geojson'],
    keywords=['python', 'geojson', 'opencv', 'contours', 'polygons'],
    readme="README.md",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ]
)
