# Adapted from $FUCHSIA_DIR/build/dart/kernel/convert_manifest_to_json.py

#!/usr/bin/env python3.8
# Copyright 2020 The Fuchsia Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
'''Reads the contents of a kernel manifest generated by the build and
  converts it to a format suitable for distribution_entries
'''

import argparse
import collections
import json
import os
import sys

Entry = collections.namedtuple('Entry', ['source', 'destination'])


def collect(lines):
    '''Reads the kernel manifest and creates an array of Entry objects.
    - lines: a list of lines from the manifest
    '''
    entries = []
    for line in lines:
        values = line.split("=", 1)
        entries.append(Entry(source=values[1], destination=values[0]))

    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--input', help='Path to original manifest', required=True)
    parser.add_argument(
        '--output', help='Path to the updated json file', required=True)
    args = parser.parse_args()

    with open(args.input, 'r') as input_file:
        contents = input_file.read().splitlines()

    entries = collect(contents)

    if entries is None:
        return 1

    with open(args.output, 'w') as output_file:
        json.dump(
            [e._asdict() for e in entries],
            output_file,
            indent=2,
            sort_keys=True,
            separators=(',', ': '))

    return 0


if __name__ == '__main__':
    sys.exit(main())
