# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clown_sort', 'clown_sort.files', 'clown_sort.util']

package_data = \
{'': ['*'], 'clown_sort': ['sorting_rules/*']}

install_requires = \
['exif>=1.5.0,<2.0.0',
 'filedate>=2.0,<3.0',
 'piexif>=1.1.3,<2.0.0',
 'pillow>=9.4.0,<10.0.0',
 'pyexiftool>=0.5.5,<0.6.0',
 'pypdf>=3.4.1,<4.0.0',
 'pytesseract>=0.3.10,<0.4.0',
 'python-dotenv>=0.21.1,<0.22.0',
 'rich-argparse-plus>=0.3.1.4,<0.4.0.0',
 'rich>=13.0.1,<14.0.0']

entry_points = \
{'console_scripts': ['set_screenshot_timestamps = '
                     'clown_sort:set_screenshot_timestamps',
                     'sort_screenshots = clown_sort:sort_screenshots']}

setup_kwargs = {
    'name': 'clown-sort',
    'version': '1.3.0',
    'description': 'Sort screenshots based on rules or through individual review.',
    'long_description': '# CLOWN SORT\nSometimes someone is being a clown on the internet. Somewhere on your hard drive is the perfect screenshot to prove to the world that the clown in question is a fool, a hypocrite, a criminal, or worse. But then - horrors - you can\'t find the screenshot! It has been lost in your vast archive of screenshots of clowns clowning themselves on the internet.\n\nClown Sort[^1] solves this.\n\n\n## What It Do\nIt sorts screenshots, PDFs, etc. based on their name and/or their textual contents into folders based on a list of rules. The contents of the tweet/reddit post/whatever are prepended to the filename and the `ImageDescription` EXIF tag is set to the OCR text. As you can configure your own arbitrary rules and run it against any set of images it works on many things other than screenshots of social media clowns, though the default configuration is for cryptocurrency clowns.\n\nFor example this screenshot of a tweet by a noteworthy cryptocurrency "reporter"[^2] on the eve of FTX\'s implosion:\n\n![](doc/larry_cermak_on_alameda_and_ftx.png)\n\nWould be renamed from `Screen Shot 2023-02-17 at 7.11.37 PM.png` to\n\n```\nTweet by @lawmaster: "I will say though before this thread gets taken over: 1. I do believe Alameda has the size to easily buy Binance\\\'s FIT OTC 2. I think the chance of FTX insolvency is near" Screen Shot 2023-02-17 at 7.11.37 PM.png\n```\n\nOther stuff that happens:\n* The `ImageDescription` EXIF tag will be written (for images).\n* All timestamps will be preserved.\n* Files that match multiple patterns will be copied to multiple destination folders.\n* The original file will be moved into a `Processed/` directory after it has been handled.\n\nNote also that:\n* This works on images that are more substantive than just self-clowning screenshots.\n* So far only Tweets and Reddit screenshots have special handling beyond OCR text extraction.\n* PDFs can be sorted by contents or filename, e.g. a PDF named `Norton Anthology of Crypto Bro Poetry.pdf` containing iambic verse like _["Fuck u justin sun  and fuck ur dick face... u all play with investing and money of the people !!!!"](https://universeodon.com/@cryptadamist/109642431382653023)_ by the noted bard JOKER_OF_CRYPTO will be copied to the `Justin Sun/` folder but not renamed.\n* Videos are not OCRed and can only be moved based on filename matches, e.g. a file called `SBF is a big fat liar.mov` will be moved to the `FTX/` folder but otherwise left alone.\n\n## Quick Start\n```sh\n# Installation with pipx is preferred if you have it but you can also use pip which comes standard\n# on almost all systems. pipx is only a noticeably better answer if you\'re a python programmer who\n# is concerned about side effects of pip upgrading system python packages.\npip install clown_sort\n\n# Get help\nsort_screenshots -h\n\n# Dry run with default cryptocurrency sort rules (dry runs don\'t actually move anything,\n# they just show you what will happen if you run again with the --execute flag)\nsort_screenshots\n\n# Execute default cryptocurrency sort rules against ~/Pictures/Screenshots\nsort_screenshots --execute\n\n# Sort a different directory of screenshots\nsort_screenshots --screenshots-dir /Users/hrollins/Pictures/get_in_the_van/tourphotos --execute\n\n# Sort with custom rules\nsort_screenshots --rules-csv /Users/hrollins/my_war.csv --execute\n\n# Sort pdfs\nsort_screenshots -f \'.*pdf$\' -e\n```\n\n# Setup\n[pipx](https://pypa.github.io/pipx/) is recommended because it keeps your system python environment safe but you can also just use `pip`.\n```\npipx install clown_sort\n```\n\n### Configuring With `.clown_sort` File\nIf there are command line options you find yourself specifying repeatedly you can place them in a `.clown_sort` file. When you invoke `sort_screenshots` the following locations will be checked for `.clown_sort`:\n\n1. The current directory\n2. Your home directory\n\nSee [the example](.clown_sort.example) for more information on what can be configured this way.\n\n### Optional Components\nIf you want to use the popup window to manually tag you _may_ need to install:\n* Python TK: `brew install python-tk@3.10` (if you don\'t have [homebrew](https://brew.sh/) you need to install it to run `brew install`)\n\nNot required for standard PNG, JPG, etc. images but you may optionally install `exiftool` for other file types if you want excessive debugging.\n* ExifTool: `brew install exiftool` or download from https://exiftool.org\n\n\n# Usage\nThe default is for the tool to run in "dry run" mode, meaning it doesn\'t actually do anything - it just shows you what it _would_ do if you added the `--execute` flag. **YOU ARE ADVISED TO MAKE A BACKUP OF YOUR SCREENSHOTS FOLDER BEFORE HITTING THE `--execute` FLAG.**\n\nWhile every effort has been made to use Python\'s cross platform `Pathlib` module as much as possible sometimes shit gets wonky on other platforms. This is 100x as true on Windows - Clown Sort has never been tested on a Windows platform.\n\n### Help Screen\n![](doc/sort_screenshots_help.png)\n\n(In my personal usuage I tend to run the tool with the `--all` and `--only-if-match` options.)\n\n### Custom Sorting Rules\nThe default is to sort cryptocurrency related content but you can define your own CSV of rules with two columns `folder` and `regex`. The value in `folder` specifies the subdirectory to sort into and `regex` is the pattern to match against. See [the default crypto related configuration](clown_sort/sorting_rules/crypto.csv) for an example. An explanation of regular expressions is beyond the scope of this README but many resources are available to help. If you\'re not good at regexes just remember that any alphanumeric string is a regex that will match that string. [pythex](http://pythex.org/) is a great website for testing your regexes.\n\n### Example Output (Automated Sorting)\n![](doc/output_example.png)\n\n\n## Manually Sorting (Experimental)\n**This is an experimental feature.** It\'s only been tested on macOS.\n\nIf you run with the `--manual-sort` command line the behavior is quite different. Rather than automatically sort files for you, instead for every file you will be greeted with a popup asking you for a desired filename and a radio button select of possible subdirectories off your `Sorted/` directory.\n\n![](doc/manual_select_box.png)\n\n\n# Contributing\nFeel free to file issues or open pull requests. Only requirement is that tests should pass before you open it, which you can check with\n\n```\npytest\n```\n\n[^1]: The name `clown_sort` was suggested by [ParrotCapital](http://twitter.com/ParrotCapital) and while the tool can work on any kind of screenshot it was too good not to use.\n\n[^2]: Perhaps notable that the "reporter" in question for years maintained a private list of the blockchain addresses of Sam Bankman-Fried\'s various scams as part of his commitment to "unrivaled transparency".\n',
    'author': 'Michel de Cryptadamus',
    'author_email': 'michel@cryptadamus.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/michelcrypt4d4mus/clown_sort',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
