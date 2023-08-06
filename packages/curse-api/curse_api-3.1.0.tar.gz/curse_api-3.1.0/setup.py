# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['curse_api', 'curse_api.clients', 'curse_api.ext']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.4,<2.0.0']

extras_require = \
{'aiohttp': ['aiohttp>=3.8.4,<4.0.0'],
 'httpx': ['httpx>=0.23.1,<0.24.0'],
 'quick': ['httpx>=0.23.1,<0.24.0']}

setup_kwargs = {
    'name': 'curse-api',
    'version': '3.1.0',
    'description': 'A simple curseforge api wrapper',
    'long_description': '# curse-api\n\n----\n\n## A simple async python Curseforge api wrapper using pydantic\n\nBuilt to serve CF endpoints while providing methods and functions to assist in finding the right mod.\n\n- Quick Install: `pip install curse-api[quick]`\n- [Features](#features)\n- [Quick Start](#quick-start)\n- [Examples](#examples)\n\n----\n\n## Some backstory\n\nA while back when I was starting to learn python further then the basics I created a small tool to download Minecraft mods from a pack manifest.\nSoon after I wrote it the new API changes came and broke it. Now once more I want to return to that project idea and expand further. After first rewriting the project using [chili](https://pypi.org/project/chili/) it felt off, so returned to rewrite once more using [pydantic](https://pypi.org/project/pydantic/) for data validation and ease of access. This is mostly a pet project to learn further python.\n\n----\n\n## Features\n\nMain Dependency:\n\n- [Pydantic](https://pypi.org/project/pydantic/)\n\nNative async library support:\n\n- [Aiohttp](https://pypi.org/project/aiohttp/) - `pip install curse-api[aiohttp]`\n- [Httpx](https://pypi.org/project/httpx/) - `pip install curse-api[httpx]`\n\nCurrently implemented:\n\n- Important endpoint support\n- Full CurseForge model\n- Mediocre error handling\n- Pluggable API factories\n- Serialization and deserialization of models\n- Python 3.7, 3.8 & 3.9 support\n- Async\n\nTo Do:\n\n- Fix to be usable with pydantic based ORM\'s\n- Address all TODO\'s\n- Test other games too\n- Add more\n- Write docs\n- Update and fix error handling\n- Shortcuts to import clients\n\nCI/CD:\n\n- Type checking\n- Version testing\n- Tests\n\n----\n\n## Examples\n\n### Quick start\n\nRequires an api from CF to use the API. You can get one [here](https://docs.curseforge.com/#authentication).\nThis example runs through most of the basics\n\n```python\nfrom curse_api import CurseAPI\nfrom curse_api.clients.httpx import HttpxFactory\nimport os\nimport asyncio\n\n\nasync def main():\n    async with CurseAPI(os.environ["CF_API_KEY"], factory=HttpxFactory) as api:\n\n        "Mods"\n        a = await api.search_mods(searchFilter="JEI", slug="jei")\n        # applies the search filters to the standard of CF docs\n\n        mod = await api.get_mod(250398)  # returns a singular Mod\n        mod_list = await api.get_mods([285109, 238222])  # returns a list of Mods\n\n        "files"\n        "See examples/download.py"\n        # TODO finish file support\n        files = await api.get_files([3940240])  # returns a list of Files matching their id\n        mod_files = await api.get_mod_files(238222)  # returns all the Files of on a give Mod\n\n        "Version details - large data"\n        "See examples/modloader.py"\n        mc = await api.minecraft_versions()  # returns all of minecraft version data\n        ml = await api.modloader_versions()  # returns **ALL** modloader versions on curseforge\n\n        mc_112 = await api.get_specific_minecraft_version("1.12.2")  # returns minecraft version related information\n        forge = await api.get_specific_minecraft_modloader("forge-36.2.39")  # returns forge related version information\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n\n### Downloading to a file\n\nThis example opens a properly named file in the current working directory and writes to it.\n\n```python\nfrom curse_api import CurseAPI\nfrom curse_api.clients.httpx import HttpxFactory\nimport os\nimport asyncio\n\n\nasync def main():\n    async with CurseAPI(os.environ["CF_API_KEY"], factory=HttpxFactory) as api:\n\n        # fetch the latest file from project with slug \'jei\'\n        mod_l, page_data = await api.search_mods(slug="jei")\n        latest = mod_l[0].latestFiles[0]\n\n        with open(latest.fileName, "wb") as f:\n            down = await api.download(latest.downloadUrl)  # type: ignore\n            async for b in down:\n                f.write(b)\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n\n```\n\n----\n\n### Sub project / extension ideas\n\n- Modloader download and installation\n- Minecraft Version type / parser\n- MC pack installation\n- DB cache extension\n- Manifest parsing\n',
    'author': 'Stinky-c',
    'author_email': '60587749+Stinky-c@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Stinky-c/curse-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
