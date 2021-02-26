"""
A tool to generate scripts using rclone to do backups.

Allows some sanity checking over your config, etc.

The scripts outputted are meant to be human readable.
"""
import copy

class BackupScript:
    """
    Our class for containing all the logic to generate the backup scripts.
    """
    def __init__(self, config):
        self.cfg = config

    def _command(self, name):
        # These ones have to be local
        src = self.cfg.lookup(name, 'src')
        if not src:
            raise RequiredNotDefined('src')

        dst = self.cfg.lookup(name, 'dst')
        if not dst:
            raise RequiredNotDefined('dst')

        command = copy.copy(self.cfg.lookup(name, 'command'))

        if self.cfg.lookup(name, 'dry_run'):
            command.append('--dry-run')

        if self.cfg.lookup(name, 'progress'):
            command.append('--progress')

        # if cfg.lookup(name, 'ignore'):
        #    command.append('--exclude-from=%s'.format())

        command.append('\"%s\"' % src)
        command.append('\"%s\"' % dst)

        return " ".join(command)

    def setup(self):
        """
        The setup needed for every script.
        """
        setup = []

        setup.append('#/bin/sh')

        description = self.cfg.description()
        if description:
            setup.append('# %s' % description.replace('\n', '\n#'))

        return setup

    def commands(self):
        """
        Builds the list of backup commands.
        """
        commands = []
        backups = self.cfg.backups()
        for name in backups:
            cmd = self._command(name)
            log_file = self.cfg.lookup(name, 'log_file')

            if self.cfg.lookup(name, 'log_file'):
                commands.append("%s 2>>%s" % (cmd, log_file))
            else:
                commands.append(cmd)

        return commands

    def generate(self):
        """
        Returns a script
        """

        setup = self.setup()
        commands = self.commands()

        return "\n".join(setup + commands)
