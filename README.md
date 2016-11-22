# Maybe reMount
Remounts unstable nfs / fuse mounts if necessary

## Usage
Configure crontab for root user `$ crontab -e`
```
0 * * * * /usr/bin/python /path/to/maybe_remount.py /mount/endpoint
```
## Note
Mount should be configured in /etc/fstab
