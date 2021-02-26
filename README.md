# Backup Script Generator

Essentially, this is a tool to generate shell scripts based on a more verbose
toml format describing what you want rclone to do.

## Usecase

This is mainly meant for producing the sort of thing you'd put into your `crontab` to do scheduled backups.

E.g, having some like the following in your crontab:
```cron
0 * * * * /home/user/bin/local_backup
0 4 * * * /home/user/bin/remote_backup
```

And the using the tool to create those two scripts.

```shell
python3 src ./examples/local.toml > /home/user/bin/local_backup
python3 src ./examples/remote.toml > /home/user/bin/remote_backup
chmod +x /home/user/bin/local_backup /home/user/bin/remote_backup
```

## Validation

Outputted scripts are meant to be human readable for verification.

The input toml goes through some stricter validation, like:

* No invalid / unknown keys are allowed.
* Types are checked against a spec.

Currently a custom checker, but a properly library for this is planned.

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
```sh
#/bin/sh
# Backups files to a b2 bucket
rclone sync --dry-run --progress --exclude ".venv" --exclude "__pycache__" \
    --exclude "*.pyc" --exclude ".flatpak-builder" --exclude "node_modules" --exclude \
    ".stack-work" --exclude "lost+found" "/mnt/user/Backups" "b2:bucket_name_here" 
```
