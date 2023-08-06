# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['baca',
 'baca.components',
 'baca.ebooks',
 'baca.resources',
 'baca.tools',
 'baca.tools.KindleUnpack',
 'baca.utils']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'beautifulsoup4>=4.12.0,<5.0.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'markdownify>=0.11.6,<0.12.0',
 'peewee>=3.16.0,<4.0.0',
 'textual>=0.16.0,<0.17.0']

entry_points = \
{'console_scripts': ['baca = baca.__main__:main']}

setup_kwargs = {
    'name': 'baca',
    'version': '0.1.13',
    'description': 'TUI Ebook Reader',
    'long_description': '# `baca`: TUI Ebook Reader\n\n![baca_fit](https://user-images.githubusercontent.com/43810055/227891952-45df1c36-5113-4793-84b6-249725d3ba19.png)\n\nMeet `baca`, [epy](https://github.com/wustho/epy)\'s lovely sister who lets you indulge\nin your favorite e-books in the comfort of your terminal.\nBut with a sleek and contemporary appearance that\'s sure to captivate you!\n\n## Features\n\n- Formats supported: Epub, Epub3, Mobi & Azw\n- Remembers last reading position\n- Scroll animations\n- Clean & modern looks\n- Lets you open images\n- Text justification\n- Dark & light colorscheme\n- Regex search\n- Hyperlinks\n\n## Requirements\n\n- `python>=3.10`\n\n## Installation\n\n- Via pip: `pip install baca`\n- Via git: `pip install git+https://github.com/wustho/baca`\n\n## Usage\n\n```sh\n# to read an ebook\nbaca path/to/your/ebook.epub\n\n# to read your last read ebook, just run baca without any argument\nbaca\n\n# to see your reading history use -r as an argument\nbaca -r\n\n# say you want to read an ebook from your reading history,\n# but you forgot the path to your ebook\n# just type any words you remember about your ebook\n# and baca will try to match it to path or title+author\nbaca doc ebook.epub\nbaca alice wonder lewis carroll\n```\n\n## Opening an Image\n\nTo open an image, when you encounter some thing like this:\n\n```\n┌──────────────────────────────────────────────────────────────────────────────┐\n│                                    IMAGE                                     │\n└──────────────────────────────────────────────────────────────────────────────┘\n```\n\njust click on it using mouse and it will open the image.\nYeah, I know you want to use keyboard for this, me too, but bear with this for now.\n\n## Configurations\n\n![pretty_yes_no_cap](https://user-images.githubusercontent.com/43810055/228417623-ac78fb84-0ee0-4930-a843-752ef693822d.png)\n\nConfiguration file available at `~/.config/baca/config.ini` for linux users. Here is the default:\n\n```ini\n[General]\n# pick your favorite image viewer\nPreferredImageViewer = auto\n\n# int or css value string like 90%%\n# (escape percent with double percent %%)\nMaxTextWidth = 80\n\n# \'justify\', \'center\', \'left\', \'right\'\nTextJustification = justify\n\n# currently using pretty=yes is slow\n# and taking huge amount of memory\nPretty = no\n\nPageScrollDuration = 0.2\n\n[Color Dark]\nBackground = #1e1e1e\nForeground = #f5f5f5\nAccent = #0178d4\n\n[Color Light]\nBackground = #f5f5f5\nForeground = #1e1e1e\nAccent = #0178d4\n\n[Keymaps]\nToggleLightDark = c\nScrollDown = down,j\nScrollUp = up,k\nPageDown = ctrl+f,pagedown,l,space\nPageUp = ctrl+b,pageup,h\nHome = home,g\nEnd = end,G\nOpenToc = tab\nOpenMetadata = M\nOpenHelp = f1\nSearchForward = slash\nSearchBackward = question_mark\nNextMatch = n\nPreviousMatch = N\nConfirm = enter\nCloseOrQuit = q,escape\nScreenshot = f12\n```\n\n## Known Limitations\n\n- When searching for specific phrases in `baca`,\n  keep in mind that it may not be able to find them if they span across two lines,\n  much like in the search behavior of editor vi(m).\n\n  For example, `baca` won\'t be able to find the phrase `"for it"` because it is split into two lines\n  in this example.\n\n  ```\n  ...\n  she had forgotten the little golden key, and when she went back to the table for\n  it, she found she could not possibly reach it: she could see  it  quite  plainly\n  ...\n  ```\n\n\n  Additionally, `baca` may struggle to locate certain phrases due to adjustments made for text justification.\n  See the example above, `"see_it"` may become `"see__it"` due to adjusted spacing between words.\n  In this case, it may be more effective to use a regex search for `"see +it"` or simply search for the word `"see"` alone.\n\n  Overall, `baca`\'s search feature is most effective for locating individual words\n  rather than phrases that may be split across multiple lines or impacted by text justification.\n\n- Compared to [epy](https://github.com/wustho/epy), currently `baca` has some missing features.\n  But these are planned to be implemented to `baca` in the near future:\n\n  - [ ] **TODO** Bookmarks\n  - [ ] **TODO** FictionBook support\n  - [ ] **TODO** URL reading support\n\n## Credits\n\n- Thanks to awesome [Textual Project](https://github.com/Textualize/textual)\n- [Kindle Unpack](https://github.com/kevinhendricks/KindleUnpack)\n- And many others!\n\n## License\n\nGPL-3\n\n',
    'author': 'Benawi Adha',
    'author_email': 'benawiadha@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
