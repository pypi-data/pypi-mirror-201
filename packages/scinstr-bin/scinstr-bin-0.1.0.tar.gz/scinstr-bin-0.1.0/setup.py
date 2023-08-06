# Set __version__ in the setup.py
with open('scinstr-bin/version.py') as f: exec(f.read())

from setuptools import setup

setup(name='scinstr-bin',
      description='Scripts to handle various scientific instruments (DMM, frequency counter, DAQ, VNA...). Need scinstr package',
      version=__version__,
      packages=['scinstr-bin'],
      scripts=[
          "bin/extract-peak",
          "bin/fswp2gnuplot",
          "bin/fswp-acq",
          "bin/gen340file",
          "bin/lakeshore-utils",
          "bin/monitor-centerone",
          "bin/monitor-cp2800",
          "bin/monitor-cryocon24c",
          "bin/monitor-lakeshore",
          "bin/monitor-pfeiffer",
          "bin/monitor-vacuum",
          "bin/mode-tracking",
          "bin/rawto340",
          "bin/t7-cli"
          ],
      install_requires=["scinstr",
                        "signalslot",
                        "PyQt5",
                        "pyqtgraph",
                        "scipy"],
      url='https://gitlab.com/bendub/scinstr-bin',
      author='Benoit Dubois',
      author_email='benoit.dubois@femto-engineering.fr',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
          'Natural Language :: English',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering'
          ]
)
