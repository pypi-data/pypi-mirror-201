from typing import Iterable, Mapping, Optional
from ..string.parse_replacement import parse_replacement
from typeguard import typechecked
from ..log import logger

import os
import shutil
import fnmatch


@typechecked
def copy_tree(
    src: str,
    dst: str,
    replacements: Optional[Mapping[str, str]] = None,
    excludes: Optional[Iterable[str]] = None
):
    if replacements is None:
        replacements = {}
    if excludes is None:
        excludes = []
    names = os.listdir(src)
    new_dst = parse_replacement(dst, replacements)
    if not os.path.exists(new_dst):
        os.makedirs(new_dst)
    for name in names:
        src_name = os.path.join(src, name)
        if any(fnmatch.fnmatch(src_name, pattern) for pattern in excludes):
            continue
        dst_name = os.path.join(dst, name)
        if os.path.isdir(src_name):
            copy_tree(src_name, dst_name, replacements, excludes)
            continue
        new_dst_name = parse_replacement(dst_name, replacements)
        shutil.copy2(src_name, new_dst_name)
        try:
            with open(new_dst_name, 'r') as file:
                file_content = file.read()
            new_file_content = parse_replacement(file_content, replacements)
            with open(new_dst_name, 'w') as file:
                file.write(new_file_content)
        except Exception:
            logger.error(f'Cannot parse file: {new_dst_name}')
