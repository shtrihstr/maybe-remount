import os
import re
import sys

class Mount:
    TEST_FILE = ".mount_test";

    _directory = None

    def __init__(self, directory):
        d = re.sub("/$", "", directory)
        if not os.path.isdir(d):
            raise ValueError("Invalid directory")
        self._directory = re.sub("/$", "", d)


    def _is_mounted(self):
        return os.path.ismount(self._directory)

    def _try_write(self):
        try:
            with open(self._get_test_file(), "w") as outfile:
                outfile.write("mount")
        except IOError:
            return False
        return True

    def _try_read(self):
        content = ""
        try:
            with open(self._get_test_file(), "rb") as outfile:
                content = outfile.read()
        except IOError:
            return False
        return content == "mount"

    def _try_remove(self):
        try:
            os.remove(self._get_test_file())
        except OSError:
            return False
        return True

    def _get_test_file(self):
        return self._directory + "/" + self.TEST_FILE;

    def is_ok(self):
        self._try_remove()
        return self._is_mounted() and self._try_write() and self._try_read() and self._try_remove()

    def _remount(self):
        escaped_dir = "'" + self._directory.replace("'", "'\\''") + "'"
        cmd = "/bin/umount -l %s && /bin/mount %s" % (escaped_dir, escaped_dir)
        os.system(cmd)

    def maybe_remount(self):
        if not self.is_ok():
            self._remount();


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError("Invalid directory")
    directory = sys.argv[1]

    mount = Mount(directory)
    mount.maybe_remount()