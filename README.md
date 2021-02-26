# Backup Script Generator

Essentially, this is a tool to generate shell scripts based on a more verbose
toml format describing what I want rclone to do.

Outputted scripts are meant to be human readable for verification.

Has some stricter validation, like:

* No invalid / unknown keys are allowed.
* Types are checked against a spec.

## Examples

Check out the [examples/](https://github.com/bahorn/backup_script/tree/master/examples)
directory for examples.

But essentially they look like this:

```toml
description = "Backups files to a b2 bucket"

[global]
ignore = [
    ".venv",
    "__pycache__",
    "*.pyc",
    ".flatpak-builder",
    "node_modules",
    ".stack-work",
    "lost+found"
]
dry_run = true
progress = true

[backups]
    [backups.remote]
    src = "/mnt/user/Backups"
    dst = "b2:bucket_name_here"
```

Which will generate something like:
```
#/bin/sh
# Backups files to a b2 bucket
rclone sync --dry-run --progress --exclude ".venv" --exclude "__pycache__" --exclude "*.pyc" --exclude ".flatpak-builder" --exclude "node_modules" --exclude ".stack-work" --exclude "lost+found" "/mnt/user/Backups" "b2:bucket_name_here"
```
