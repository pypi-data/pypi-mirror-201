import setuptools
import poliduckie_segmentation
with open("README.md", "r", encoding="utf-8") as fh:
  README = fh.read()
version = poliduckie_segmentation.__version__
setuptools.setup(
  name = 'poliduckie_segmentation',
  packages = ['poliduckie_segmentation'],
  version = version,
  license="""MIT""",
  description = """Segmentation from the Poliduckie team.""",
  long_description_content_type="text/markdown",
  long_description=README,
  author = 'Poliduckies',
  author_email = 'duckietown@aeapolimi.it',
  url = 'https://github.com/poliduckie/poliduckie_segmentation',
  # download_url = 'https://github.com/poliduckies/poliduckie_segmentation/archive/refs/tags/v'+version+'-alpha.tar.gz',
  keywords = ['segmentation', 'duckietown', 'tensorflow'],
  install_requires=[
          'tensorflow',
          'casadi',
          'numpy',
          'opencv-python'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
  python_requires=">=3.6",
  package_data = {
    'poliduckie_segmentation': ['*']
  },
  include_package_data=True,
)
