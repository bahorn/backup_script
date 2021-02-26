"""
Core code behind the tool, implementing the main logic behind it.
"""
import copy


def readable_lines(cmd):
    """
    Goes through and places new lines to split up a command to make it
    readable.
    """
    result = ""
    line_length = 0
    for section in cmd:
        if line_length + len(section) + 8 > 80:
            line_length = 4
            result += '\\\n'
            result += ' ' * line_length
            result += section + ' '
        else:
            line_length += len(section)
            result += section + ' '

    return result

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

        if self.cfg.lookup(name, 'ignore'):
            for item in self.cfg.lookup(name, 'ignore'):
                command.append('--exclude')
                command.append('\"%s\"' % item)

        command.append('\"%s\"' % src)
        command.append('\"%s\"' % dst)

        return readable_lines(command)

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
