from setuptools import setup

short_description = """A Python package to simplify the deployment process of exported
    Teachable Machine models into different into different Robotics, AI and IoT controllers such as: Raspberry Pi, Jetson Nano
    and any other SBCs using TensorFlowLite framework."""

with open("README.md", "r") as desc:
    long_description = desc.read()

setup(
    name="teachable-machine-lite",
    version="1.1",
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["teachable_machine_lite"],
    package_dir={"": "src"},
    readme="README.md",
    url="https://github.com/MeqdadDev/teachable-machine-lite",
    author="Meqdad Dev",
    author_email="meqdad.darweesh@gmail.com",
    install_requires=['numpy', 'tflite-runtime', 'Pillow'],
    keywords=['python', 'teachable machine', 'ai', 'computer vision',
              'camera', 'opencv', 'image classification', 'tensorflowlite', 'raspberry pi'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Artificial Life",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Utilities",
    ],
)
