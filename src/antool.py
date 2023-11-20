#!/usr/bin/env python
from pprint import pprint
import sys

from anclient import ActionNetworkClient


def main(argv):
    an = ActionNetworkClient()
    r = an._do_get(argv[0])
    pprint(r)

if __name__ == "__main__":
    main(sys.argv[1:])
