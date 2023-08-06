import setuptools

setuptools.setup(
    name="homeline",
    version="1.0.0",
    author="Magnus Eldén",
    description="Wrapper for the Compare It Homeline Api",
    packages=["Compare_It"],
    install_requires=[
          'requests',
      ],
)   