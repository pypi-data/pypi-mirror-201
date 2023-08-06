import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyAudioCensor", 
    version="0.0.1",
    author="Mayukhmali Das",
    description="Automated Offline Censoring of Audio Files using Vosk and Python.",
    python_requires='>=3.6'
)