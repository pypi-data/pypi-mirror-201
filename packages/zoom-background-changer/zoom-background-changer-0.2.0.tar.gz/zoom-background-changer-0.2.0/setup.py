# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zoom_background_changer']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.27.4,<0.28.0']

entry_points = \
{'console_scripts': ['zoom-background-changer = '
                     'zoom_background_changer.main:main']}

setup_kwargs = {
    'name': 'zoom-background-changer',
    'version': '0.2.0',
    'description': 'Changes your Zoom background using OpenAI Image Generation.',
    'long_description': '# Zoom Background Changer\n\nThis is a python script that will use OpenAI\'s GPT-3 API to generate a new background image for your Zoom meetings.\n\nIt can be run as a cron task, manually, or as part of a workflow when you open Zoom!\n\nThe script will generate a new background image based on the current date and weather, and overwrite you existing Zoom background.\n\n## Requirements\n\n- Only works on macOS (for now!)\n- Python 3.9+\n- OpenAI API Key\n  - You can get a free API key from OpenAI [here](https://platform.openai.com/).\n  - You will need to create an account and generate an API key.\n  - You will need to add your API key to the `OPENAI_API_KEY` environment variable.\n\n## Installation\n\n```bash\npip install zoom-background-changer\n```\n\n## Usage\n\nFirst you will need to set a custom background image in Zoom.\n\nYou can do this by going to `Preferences > Video > Virtual Background > Choose Virtual Background...` and selecting an image.\n\nThen from the command line, run:\n```bash\nzoom-background-changer\n```\n\n## Prompt Template\n\nCan be adjusted by creating a file called `.zoom-background-changer` in your `$HOME` directory.\n\nThis file should contain the following:\n\n```json\n{\n  "prompt": "Today is {date} and the weather is {weather} in {city}.",\n  "city": "Boston"\n}\n```\n\n### Available Variables\n\n- `{date}`: The current date\n- `{city}`: The current city, set from the `city` key in the `.zoom-background-changer` file. Defaults to `Boston, MA`. If set, the following extra variables will be available:\n  - `{weather}`: The current weather, from `https://wttr.in/`\n  - `{temperature}`: The current temperature, from `https://wttr.in/`\n\nAny other key/value pairs in the `.zoom-background-changer` file will be available as variables in the prompt template, so get creative!\n\nIf you would like to request a new functional variable similar to `city`, please open an Issue or Pull Request!\n',
    'author': 'Kyle Montag',
    'author_email': 'thekylemontag@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
