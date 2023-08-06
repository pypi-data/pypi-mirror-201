# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ds_caselaw_utils']

package_data = \
{'': ['*'], 'ds_caselaw_utils': ['data/*']}

install_requires = \
['ruamel.yaml>=0.17.21,<0.18.0']

setup_kwargs = {
    'name': 'ds-caselaw-utils',
    'version': '0.5.0',
    'description': 'Utilities for the National Archives Caselaw project',
    'long_description': '# The National Archives: Find Case Law\n\nThis repository is part of the [Find Case Law](https://caselaw.nationalarchives.gov.uk/) project at [The National Archives](https://www.nationalarchives.gov.uk/). For more information on the project, check [the documentation](https://github.com/nationalarchives/ds-find-caselaw-docs).\n\n# Python Utilities\n\n![PyPI](https://img.shields.io/pypi/v/ds-caselaw-utils) ![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/ds-caselaw-utils)\n\nThis repository contains common functions used throughout the National Archives Caselaw project, reducing duplication and complexity.\n\npypi name: [ds-caselaw-utils](https://pypi.org/project/ds-caselaw-utils)\npython import name: `ds_caselaw_utils`\n\n## Examples\n\n```\nfrom ds_caselaw_utils import neutral_url\nneutral_url("[2022] EAT 1")  # \'/eat/2022/4\'\n\nfrom ds_caselaw_utils import courts\n\ncourts.get_all() # return a list of all courts\n\ncourts.get_by_param("ewhc/ch") # get a court by its parameter value\n\ncourts.get_selectable() # returns a list of all courts that are whitelisted to\n                        # appear as searchable options\n\ncourts.get_listable_groups() # returns a grouped list of courts that are whitelisted to\n                             # be listed publicly\n\ncourts.get_listable_courts() # returns a list of all *courts* (ie not tribunals)\n                             # which are whitelisted to be listed publicly\n\ncourts.get_listable_tribunals() # return a list of all *tribunals*  which are\n                                # whitelisted to be listed publicly\n\n\n```\n\nThe list of courts is defined in `src/ds_caselaw_utils/data/court_names.yml`. The format is as follows:\n\n```\n- name: high_court # Internal name of a group of courts to be displayed together\n  display_name: "High Court" # An optional public facing name for this group.\n  is_tribunal: false # Whether this group contains courts or tribunals\n  courts: # List of courts to be displayed under this group\n    -\n        # An internal code for this court:\n        code: EWHC-SeniorCourtsCosts\n         # The public facing name of the court:\n        name: Senior Courts Costs Office\n        # An alternative wording for use in listings (optional, defaults to `name`)\n        list_name: High Court (Senior Court Costs Office)\n        # A URL to link to for more information on this court:\n        link: https://www.gov.uk/courts-tribunals/senior-courts-costs-office\n        # A regex matching neutral citations for this court\'s judgments:\n        ncn: \\[(\\d{4})\\] (EWHC) (\\d+) \\((SCCO)\\)\n        # The canonical parameter value used in searches for this court:\n        param: \'ewhc/scco\'\n        # Any additional parameter aliases which display judgments from this court:\n        extra_params: [\'ewhc/costs\']\n        # The year of the first judgment we have on file for this court:\n        start_year: 2003\n        # The year of the last judgment we have on file for this court\n        # (optional, defaults to current year):\n        end_year: ~\n        # Whether to expose this court publicly as selectable in search filters:\n        selectable: true\n        # Whether to expose this court publicly in listings:\n        listable: true\n```\n\n## Testing\n\n```bash\n$ poetry shell\n$ cd src/ds_caselaw_utils\n$ python -m unittest\n```\n\n## Building\n\n```bash\n$ rm -rf dist\n$ poetry build\n$ python3 -m twine upload --repository testpypi dist/* --verbose\n```\n\n## Releasing\n\nWhen making a new release, update the [changelog](CHANGELOG.md) in the release\npull request.\n\nThe package will **only** be released to PyPI if the branch is tagged. A merge\nto main alone will **not** trigger a release to PyPI.\n\nTo create a release:\n\n0. Update the version number in `pyproject.toml`\n1. Create a branch `release/v{major}.{minor}.{patch}`\n2. Update `CHANGELOG.md` and `pyproject.toml` for the release\n3. Commit and push\n4. Open a PR from that branch to main\n5. Get approval on the PR\n6. Tag the HEAD of the PR `v{major}.{minor}.{patch}` and push the tag\n7. Merge the PR to main and push\n8. Add a new release to Github for that tag for consistency\'s sake\n',
    'author': 'Nick Jackson',
    'author_email': 'nick@dxw.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nationalarchives/ds-caselaw-utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
