# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vt2m', 'vt2m.lib', 'vt2m.subcommands']

package_data = \
{'': ['*']}

install_requires = \
['pymisp>=2.4.169.3,<3.0.0.0',
 'requests>=2.27.1,<3.0.0',
 'typer>=0.7.0,<0.8.0',
 'vt-py>=0.17.4,<0.18.0']

entry_points = \
{'console_scripts': ['vt2m = vt2m.main:app']}

setup_kwargs = {
    'name': 'vt2m',
    'version': '0.1.11',
    'description': 'Automatically import results from VirusTotal queries into MISP objects',
    'long_description': '# VirusTotal Query to MISP Objects (vt2m)\n\nWhile there are multiple Python projects which implement the object creation based on single VirusTotal objects, this\nproject aims to enable users to directly convert VirusTotal search queries to MISP objects.\n**This is work in progress.** Future release will implement handling URLs, Domain and IP objects, too. Right now, only\nfile objects - as a base for queries - are implemented. These file objects can have related IPs, domains and URLs, though.\n\n## Installation\n\n```\npip install vt2m\n```\n\n## Usage\n\nIf you use the script frequently, passing the arguments as environment variables (`MISP_URL`, `MISP_KEY`, `VT_KEY`)\ncan be useful to save some time. For example, this can be achieved through creating a shell script which passes the\nenvironment variables and executes the command with spaces in front, so it does not show up in the shell history. Something like this:\n\n```bash\n#!/usr/bin env bash\n\nSAVEIFS=$IFS\nIFS=$(echo -en "\\n\\b")\nIFS=$SAVEIFS\n    MISP_URL="https://my.misp.host.local" MISP_KEY="MyMISPApiKey1234567890" VT_KEY="MyVTApiKey1234567890" /path/to/venv/bin/vt2m "$@"\nIFS=$SAVEIFS\n```\n\nChanging the IFS is a must, so spaces are not seen as a field seperator.\n\nOverall, `vt2m` supports three commands:\n\n- VirusTotal Intelligence Search via `query`\n- Accessing Live Hunting notifications via `notifications` (or `no`)\n- Accessing Retrohunt results via `retrohunts` (or `re`)\n\n### VirusTotal Ingelligence Search: `query`\n\n```\nUsage: vt2m query [OPTIONS] QUERY\n\n  Query VT for files and add them to a MISP event\n\nArguments:\n  QUERY  VirusTotal Query  [required]\n\nOptions:\n  -u, --uuid TEXT                MISP event UUID  [required]\n  -U, --url TEXT                 MISP URL - can be passed via MISP_URL env\n  -K, --key TEXT                 MISP API Key - can be passed via MISP_KEY env\n  -k, --vt-key TEXT              VirusTotal API Key - can be passed via VT_KEY\n                                 env\n  -c, --comment TEXT             Comment for new MISP objects.\n  -l, --limit INTEGER            Limit of VirusTotal objects to receive\n                                 [default: 100]\n  -L, --limit-relations INTEGER  Limit the amount of related objects. Note\n                                 that this is for every relation queries.\n                                 [default: 40]\n  -r, --relations TEXT           Relations to resolve via VirusTotal,\n                                 available relations are: execution_parents,\n                                 compressed_parents, bundled_files,\n                                 dropped_files, contacted_urls, embedded_urls,\n                                 itw_urls, contacted_domains,\n                                 embedded_domains, itw_domains, contacted_ips,\n                                 embedded_ips, itw_ips, submissions,\n                                 communicating_files\n  -d, --detections INTEGER       Amount of detections a related VirusTotal\n                                 object must at least have  [default: 0]\n  -D, --extract-domains          Extract domains from URL objects and add them\n                                 as related object.\n  -f, --filter TEXT              Filtering related objects by matching this\n                                 string(s) against json dumps of the objects.\n  -p, --pivot TEXT               Pivot from the given query before resolving\n                                 relationships. This must be a valid VT file\n                                 relation (execution_parents,\n                                 compressed_parents, bundled_files,\n                                 dropped_files).\n  -P, --pivot-limit INTEGER      Limit the amount of files returned by a\n                                 pivot.  [default: 40]\n  -C, --pivot-comment TEXT       Comment to add to the initial pivot object.\n  --pivot-relationship TEXT      MISP relationship type for the relation\n                                 between the initial pivot object and the\n                                 results.  [default: related-to]\n  --help                         Show this message and exit.\n```\n\nThe `query` command supports ingesting files from a VT search, but additional also requesting specific related files or infrastructure indicators (via `--relations`) and an initial pivot off the files (via `--pivot`). The latter means that, e.g., you\'re able to search for files that are commonly dropped or contained within the samples you\'re actually searching for and use the "parent" files as your regular result set, enrichting them with additional relationships etc.\n\nVia `--relations` VirusTotal relations can be resolved and added as MISP objects with the specific relations, e.g. the\nfollowing graph was created using vt2m:\n![MISP Graph](.github/screenshots/graph.png)\n*Graph created via `vt2m --uuid <UUID> --limit 5 --relations dropped_files,execution_parents "behaviour_processes:\\"ping -n 70\\""`*\n\n### VirusTotal Livehunt notifications: `notifications`\n\n```\nUsage: vt2m notifications [OPTIONS] COMMAND [ARGS]...\n\n  Query and process VT notifications\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  import  Import files related to notifications\n  list    List currently available VirusTotal notifications\n```\n\nThe command allows to list and to import livehunt results via two subcommands.\n\n### VirusTotal Retrohunt results: `retrohunts`\n\n```\nUsage: vt2m retrohunts [OPTIONS] COMMAND [ARGS]...\n\n  Query for retrohunt results.\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  import  Imports results of a retrohunt into a MISP event\n  list    Lists available retrohunts\n```\n\nThe command allows to list and to import retrohunt results via two subcommands.\n',
    'author': '3c7',
    'author_email': '3c7@posteo.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/3c7/vt2m',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
