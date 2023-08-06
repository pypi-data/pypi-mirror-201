import setuptools

setuptools.setup(
    name="homeline",
    version="2.0.1",
    author="Magnus Eldén",
    description="Wrapper for the Compare It Homeline Api",
    packages=["Compare_It"],
    install_requires=[
          'requests',
      ],
)   