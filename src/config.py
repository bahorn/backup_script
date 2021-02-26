"""
A tool to generate scripts using rclone to do backups.

Allows some sanity checking over your config, etc.

The scripts outputted are meant to be human readable.
"""
from spec import validate, Spec, SpecTypes

class RequiredNotDefined(Exception):
    """
    Custom exception for handling the case where a required option in the
    config is not defined.
    """
    def __init__(self, name):
        self.name = name
        super().__init__()

    def __str__(self):
        return "%s is not defined in the config" % self.name


class ConfigInvalid(Exception):
    """
    Exception for signaling invalid configurations.
    """
    def __init__(self, name):
        self.name = name
        super().__init__()

    def __str__(self):
        return self.name


class Config:
    """
    Container class for the configuration, allowing lookups in our preferred
    order.
    """
    defaults = {
        'command': ['rclone', 'sync'],
        'dry_run': True,
        'progress': True,
        'ignore': []
    }

    # Format spec
    format_spec = {
        'description': (Spec.OPTIONAL, SpecTypes.STRING),
        'global': (
            Spec.OPTIONAL,
            {
                'ignore': (Spec.OPTIONAL, SpecTypes.STR_LIST),
                'dry_run': (Spec.OPTIONAL, SpecTypes.BOOL),
                'progress': (Spec.OPTIONAL, SpecTypes.BOOL),
            }
        ),
        'backups': (
            Spec.HASH,
            {
                'src': (Spec.REQUIRED, SpecTypes.STRING),
                'dst': (Spec.REQUIRED, SpecTypes.STRING)
            }
        )
    }

    def __init__(self, config):
        self.config = config
        if not self.validate():
            raise ConfigInvalid('invalid config')
        self.globalcfg = config.get('global', {})

    def base(self, prop):
        """
        Looks up in the global configuration.
        """
        globalp = self.globalcfg.get(prop, None)

        if globalp:
            return globalp

        return self.defaults.get(prop)

    def lookup(self, section, prop):
        """
        Function to lookup the value of settings, in our preference order.
        """
        backups = {}

        if section:
            backups = self.backups()[section]

        localp = backups.get(prop, None)

        if localp:
            return localp

        return self.base(prop)

    def backups(self):
        """
        Just return the list of backup sections.
        """
        return self.config['backups']

    def description(self):
        """
        Return a name defined in the configuration.
        """
        return self.config.get('description', None)

    def validate(self):
        """
        Verifies the configuration format is correct.

        This does things such as checking for configuration options that aren't
        defined in the format, etc.
        """

        return validate(self.config, self.format_spec)
