#!/usr/bin/python

import sys
import warnings

warnings.filterwarnings("ignore")

if __name__ == "__main__":
	from pylint import lint
	lint.Run(sys.argv[1:])

