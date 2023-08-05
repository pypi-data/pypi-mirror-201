from distutils.core import setup
setup(
  include_package_data=True,
  #package_dir={"": "slue_evaluator"},
  name = 'slue_evaluator',         # How you named your package folder (MyLib)
  packages = ['slue_evaluator'],   # Chose the same as "name"
  version = '0.8',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = "Evalutes the model's output on slue dataset",   # Give a short description about your library
  author = 'RAGHU DINESH',                   # Type in your name
  author_email = 'raghudinesh98@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/RAGHUDINESH/slue_evaluator',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/RAGHUDINESH/slue_evaluator/archive/refs/tags/v_01.tar.gz',    # I explain this later on
  keywords = ['E2E','EVALUATION','NER'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'editdistance',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',

  ],
)