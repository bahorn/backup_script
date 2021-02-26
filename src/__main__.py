"""
A tool to generate scripts using rclone to do backups.

Allows some sanity checking over your config, etc.

The scripts outputted are meant to be human readable.
"""
import sys
import toml
from config import Config
from tool import BackupScript


def main(args):
    """
    Entry point for the tool
    """
    cfg_f = toml.load(open(args[1], 'r'))
    cfg = Config(cfg_f)
    script_generator = BackupScript(cfg)
    return script_generator.generate()


if __name__ == '__main__':
    print(main(sys.argv))
