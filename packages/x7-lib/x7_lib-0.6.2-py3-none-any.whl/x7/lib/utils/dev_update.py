"""
    Update various development files::

    % python -m x7.lib.utils.dev_update <file>...
"""

import os.path
import sys
from hashlib import md5

CHECKSUM_TAG = '# DO NOT EDIT: copied via dev_update. Checksum: '
VALID_UPDATE_FILES = (
    # 'dev-update-test.txt',
    '.gitignore',
    'common.mk',
    'dev-requirements.txt',
    'docs/conf.py',
    'docs/Makefile',
)
VERBOSE = False


class FileChanged(Exception):
    """File to update has changed since last update"""
    pass


class BadFilename(Exception):
    """Invalid file name or path"""
    pass


def do_checksum(data: str) -> str:
    return md5(data.encode('utf-8')).hexdigest()


def update_file(name: str) -> None:
    if 'x7-lib' in os.getcwd():
        raise BadFilename('Do not run dev_update from x7-lib project')
    if name not in VALID_UPDATE_FILES:
        raise BadFilename('%s: Can only update one of %s' % (name, ', '.join(VALID_UPDATE_FILES)))
    orig_checksum = None
    if os.path.exists(name):
        # Verify that it is unmodified
        data = open(name, 'r').read()
        checksum, nl, filedata = data.partition('\n')
        if not checksum.startswith(CHECKSUM_TAG):
            raise FileChanged('%s: No checksum line found' % name)
        checksum_val = checksum[len(CHECKSUM_TAG):].strip()
        if filedata.startswith('\n'):
            filedata = filedata[1:]
        orig_checksum = do_checksum(filedata)
        if checksum_val != orig_checksum:
            raise FileChanged('%s: Checksum mismatch: %s vs %s (calc)' % (name, checksum_val, orig_checksum))
        if VERBOSE:
            print('update ok: checksum matches: %s' % name)
    else:
        if VERBOSE:
            print('update ok: does not exist: %s' % name)

    lib_file = '../x7-lib/' + name
    filedata = open(lib_file, 'r').read()
    new_checksum = do_checksum(filedata)
    if new_checksum == orig_checksum:
        if VERBOSE:
            print('update skipped: file not changed: %s' % name)
    else:
        with open(name, 'w') as dev_file:
            dev_file.write('%s%s\n\n' % (CHECKSUM_TAG, new_checksum))
            dev_file.write(filedata)
        print('updated: %s (%s)' % (name, new_checksum))


def main():
    if sys.argv[1:]:
        names = sys.argv[1:]
    else:
        names = VALID_UPDATE_FILES
    try:
        for name in names:
            update_file(name)
    except FileChanged as bad_name:
        print('ERROR: %s' % bad_name)
        print('File has changed locally. Check changes and delete the file to allow update')
        exit(1)
    except BadFilename as bad_dir:
        print('ERROR: %s' % bad_dir)
        exit(1)


if __name__ == '__main__':
    main()
