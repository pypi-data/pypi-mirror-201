import subprocess as _subprocess
import argparse as _argparse


parser = _argparse.ArgumentParser(
    fromfile_prefix_chars="@", 
    add_help=False,
) # prefix_chars="",)
parser.add_argument('searchterm')
parser.add_argument('auxarg', nargs='*')


def main():
    ns, args = parser.parse_known_args()
    _subprocess.run(["find", "-name", f"*{ns.searchterm}*"] + args, check=True)


if __name__ == '__main__':
    main()






