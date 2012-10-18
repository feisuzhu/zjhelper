#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    node = os.uname()[1].replace('.', '_').lower()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zjhelper.settings_%s" % node)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
