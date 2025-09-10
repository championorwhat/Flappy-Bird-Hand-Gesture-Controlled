"""
Setup script for Hand Gesture Flappy Bird
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="hand-gesture-flappy-bird",
    version="1.0.0",
    author="AI Assistant",
    description="A Flappy Bird game controlled by hand gestures using MediaPipe",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: pygame",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "hand-flappy-bird=main:main",
        ],
    },
    keywords="game, flappy bird, hand gesture, computer vision, mediapipe, pygame",
    project_urls={
        "Bug Reports": "https://github.com/your-username/hand-gesture-flappy-bird/issues",
        "Source": "https://github.com/your-username/hand-gesture-flappy-bird",
    },
)