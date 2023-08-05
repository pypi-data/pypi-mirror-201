# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dir2md']
install_requires = \
['fire>=0.5.0,<0.6.0', 'funcparserlib>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['dir2md = dir2md:dir2md_cli',
                     'md2dir = dir2md:md2dir_cli']}

setup_kwargs = {
    'name': 'dir2md',
    'version': '0.3.1',
    'description': '',
    'long_description': '# dir2md\n\n`dir2md` is a command-line tool that converts directories of files into Markdown code blocks. It also provides a reverse function, md2dir, which converts Markdown code blocks back into their original files.\n\n## Installation\n\nInstall `dir2md` using `pip`:\n\n```bash\npip install dir2md\n```\n\n## Usage\n\n`dir2md` can be used as a command-line tool or imported as a module.\n\n### Command-Line Tool\n\nTo convert a directory of files to Markdown code blocks, run:\n\n```bash\ndir2md [files...]\n```\n\nThis will print the resulting Markdown to the console.\n\nTo convert Markdown code blocks back into their original files, run:\n\n```bash\nmd2dir [options] \n```\n\nThis will create the files in the current working directory.\n\nFor more options and usage details, use the `--help` flag.\n\n### Module\n\n```bash\nimport dir2md\n\n# Convert a directory of files to Markdown code blocks\nmarkdown = dir2md.dir2md("file1.py", "file2.py")\n\n# Convert Markdown code blocks back into their original files\ndir2md.md2dir_save(markdown, output_dir="output/")\n```\n\n### Wildcard support\n\nYou can use wildcards (`*`) to pass multiple files at once.\n\nFor example, to include all Python files in the current directory:\n\n```bash\ndir2md *.py\n```\n\nTo do so recursively, use `**`:\n\n```bash\ndir2md **/*.py\n```\n\n`dir2md` uses `glob` to parse your path pattern. To turn this off, use the `--no-glob` flag.\n\n#### Truncation\n\n`dir2md` now supports truncating long files with the `{start_line,end_line}` syntax added to the file or directory path.\n\nFor example:\n\n- Get the first 10 lines of a file: `dir2md "path/to/file.py[:10]"`\n- Get lines 10 to 20: `dir2md "path/to/file.py[10:20]"`\n- Get everything from line 10 until the end of the file: `dir2md "path/to/file.py[10:]"`\n- Get the first 10 lines of a file followed by an ellpsis: `dir2md "path/to/file.py[:10...]"`\n- Negative indices: `dir2md "path/to/file.py[-10:]"`\n- Multiple truncations: `dir2md "path/to/file.py[:10 20:]"`\n- Omit the entire contents of the file with an ellipsis: `dir2md "path/to/file.py[..]"`\n\nThis syntax can be used with wildcards as well.\n\nThe quotation marks are required to prevent your shell from interpreting the brackets as special characters.\n\n```bash\ndir2md *.py[:10]   # First 10 lines of all .py files\ndir2md **/*.py[5:]  # All lines after the first 5 lines in all .py files recursively\n```\n\n### Handling missing files\n\nYou can customize the behavior when a specified file is not found using the `on_missing` option. By default, it is set to `"error"` which will raise a `FileNotFoundError`. To ignore the missing file and continue processing other files, pass `on_missing="ignore"` as an argument to the `dir2md` function.\n\n```python\ndir2md("missing_file.py", on_missing="ignore")\n```\n',
    'author': 'IsaacBreen',
    'author_email': 'mail@isaacbreen.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
