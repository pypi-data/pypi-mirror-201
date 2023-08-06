
import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="AI-TTS",
    version="0.0.1",
    author="WhyFenceCode",
    author_email="whyfencecode@gmail.com",
    packages=["AI_TTS"],
    description="An easy way to use AI TTS",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/WhyFenceCode/AI-Voice",
    license='MIT',
    python_requires='>=3.8',
    install_requires=[]
)
