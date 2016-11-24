import os
import re
import subprocess
import sys
import logging

class Mount:
    _directory = None

    def __init__(self, directory):
        self._directory = re.sub("/$", "", directory)
        if not os.path.isdir(self._directory):
            raise ValueError("Invalid directory")

        if self._directory not in open("/etc/fstab", "r").read():
            raise ValueError("Invalid mount endpoint")

    def _is_mounted(self):
        return os.path.ismount(self._directory)

    def _is_alive(self):
        escaped_dir = "'" + self._directory.replace("'", "'\\''") + "'"
        cmd = "/usr/bin/timeout 5 ls %s || echo 'timeout'" % escaped_dir;
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE);
        output = p.communicate()[0];
        return output != "timeout\n"

    def is_ok(self):
        return self._is_mounted() and self._is_alive()

    def _remount(self):
        escaped_dir = "'" + self._directory.replace("'", "'\\''") + "'"
        os.system("/bin/umount -l %s" % escaped_dir)
        os.system("/bin/mount -l %s" % escaped_dir)
        logging.info("Remount %s" % self._directory)

    def maybe_remount(self):
        if not self.is_ok():
            self._remount();

if __name__ == '__main__':

    logging.basicConfig(filename="/var/log/maybe_remount.log", level=logging.INFO, format='%(asctime)s %(message)s')

    if len(sys.argv) < 2:
        raise ValueError("Invalid directory")

    directory = sys.argv[1]

    mount = Mount(directory)
    mount.maybe_remount()