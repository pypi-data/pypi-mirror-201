# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kor', 'kor.encoders']

package_data = \
{'': ['*']}

install_requires = \
['langchain>=0.0.110', 'openai>=0.27,<0.28', 'pandas>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'kor',
    'version': '0.7.0',
    'description': 'Extract information with LLMs from text',
    'long_description': '**⚠ WARNING: Prototype with unstable API. 🚧**  \n\n[![Unit Tests](https://github.com/eyurtsev/kor/actions/workflows/test.yml/badge.svg?branch=main&event=push)](https://github.com/eyurtsev/kor/actions/workflows/test.yml)\n[![Test Docs](https://github.com/eyurtsev/kor/actions/workflows/doc_test.yaml/badge.svg?branch=main&event=push)](https://github.com/eyurtsev/kor/actions/workflows/doc_test.yaml)\n\n# Kor\n\n\nThis is a half-baked prototype that "helps" you extract structured data from text using LLMs 🧩.\n\nSpecify the schema of what should be extracted and provide some examples.\n\nKor will generate a prompt, send it to the specified LLM and parse out the\noutput. \n\nYou might even get results back.\n\nSee [documentation](https://eyurtsev.github.io/kor/).\n\n## Version >=0.4.0\n\n* Integrated with langchain framework.\n* The code below uses Kor style schema, but you can also use [pydantic](https://eyurtsev.github.io/kor/validation.html).\n\n\n```python\n\n  from langchain.chat_models import ChatOpenAI\n  from kor import create_extraction_chain, Object, Text, Number\n\n  llm = ChatOpenAI(\n      model_name="gpt-3.5-turbo",\n      temperature=0,\n      max_tokens=2000,\n      frequency_penalty=0,\n      presence_penalty=0,\n      top_p=1.0,\n  )\n\n  schema = Object(\n    id="player",\n    description=(\n        "User is controling a music player to select songs, pause or start them or play"\n        " music by a particular artist."\n    ),\n    attributes=[\n        Text(\n            id="song",\n            description="User wants to play this song",\n            examples=[],\n            many=True,\n        ),\n        Text(\n            id="album",\n            description="User wants to play this album",\n            examples=[],\n            many=True,\n        ),\n        Text(\n            id="artist",\n            description="Music by the given artist",\n            examples=[("Songs by paul simon", "paul simon")],\n            many=True,\n        ),\n        Text(\n            id="action",\n            description="Action to take one of: `play`, `stop`, `next`, `previous`.",\n            examples=[\n                ("Please stop the music", "stop"),\n                ("play something", "play"),\n                ("play a song", "play"),\n                ("next song", "next"),\n            ],\n        ),\n    ],\n    many=False,\n)\n\n  chain = create_extraction_chain(llm, schema, encoder_or_encoder_class=\'json\')\n  chain.predict_and_parse(text="play songs by paul simon and led zeppelin and the doors")[\'data\']\n```\n\n```python\n  {\'player\': {\'artist\': [\'paul simon\', \'led zeppelin\', \'the doors\']}}\n```\n\n## Compatibility\n\n`Kor` is tested against python 3.8, 3.9, 3.10, 3.11.\n\n## Installaton \n\n```sh\npip install kor\n```\n\n## 💡 Ideas\n\nIdeas of some things that could be done with Kor.\n\n* Extract data from text that matches an extraction schema.\n* Power an AI assistant with skills by precisely understanding a user request.\n* Provide natural language access to an existing API.\n\n## 🚧 Prototype\n\nPrototype! So the API is not expected to be stable!\n\n##  ✨ What does Kor excel at?  🌟 \n\n* Making mistakes! Plenty of them!\n* Slow! It uses large prompts with examples, and works best with the larger slower LLMs.\n* Crashing for long enough pieces of text! Context length window could become\n  limiting when working with large forms or long text inputs.\n\nThe expectation is that as LLMs improve some of these issues will be mitigated.\n\n## Limtations\n\nNo limitations whatsoever. Do take a look at the section directly above as well\nas at the section about compatibility.\n\n## Potential Changes\n\n* Adding validators\n* Built-in components to quickly assemble schema with examples\n* Add routing layer to select appropriate extraction schema for a use case when\n  many schema exist\n\n## 🎶 Why the name?\n\nFast to type and sufficiently unique.\n\n## Contributing\n\nIf you have any ideas or feature requests, please open an issue and share!\n\nSee [CONTRIBUTING.md](https://github.com/eyurtsev/kor/blob/main/CONTRIBUTING.md) for more information.\n\n## Other packages\n\nProbabilistically speaking this package is unlikely to work for your use case.\n\nSo here are some great alternatives:\n\n* [Promptify](https://github.com/promptslab/Promptify)\n* [MiniChain](https://srush.github.io/MiniChain/examples/stats/)\n',
    'author': 'Eugene Yurtsev',
    'author_email': 'eyurtsev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.github.com/eyurtsev/kor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
