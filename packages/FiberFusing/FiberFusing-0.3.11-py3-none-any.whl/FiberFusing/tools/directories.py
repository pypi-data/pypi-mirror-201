#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import FiberFusing


root_path = Path(FiberFusing.__path__[0])

project_path = root_path.parents[0]

example_directory = root_path.joinpath('examples')

doc_path = root_path.parents[0].joinpath('docs')

doc_css_path = doc_path.joinpath('source/_static/default.css')

style_directory = root_path.joinpath('styles')

logo_path = doc_path.joinpath('images/logo.png')

version_path = root_path.joinpath('VERSION')

examples_path = root_path.joinpath('examples')


if __name__ == '__main__':
    path_list = [
        root_path,
        project_path,
        example_directory,
        doc_path,
        doc_css_path,
        style_directory,
        logo_path,
        version_path,
        examples_path
    ]

    for path in path_list:
        print(path, path.exists())

# -
