import os
import sys


class FilePathHelper():

    @staticmethod
    def convert_to_absolute_path(file_path):
        if not os.path.isabs(file_path):
            return "{0}\\{1}".format(os.getcwd(), file_path)
        return file_path

    @staticmethod
    def get_is_absolute_path(file_path):
        return os.path.isabs(file_path)

    @staticmethod
    def is_valid_file_path(file_path):
        return os.path.isfile(file_path) and os.path.exists(file_path)

    @staticmethod
    def is_valid_file_ext(file_path, valid_extensions_list):
        valid_list = set([e.lower() for e in valid_extensions_list])
        ext = os.path.splitext(file_path)[-1]
        return ext in valid_list

    @staticmethod
    def get_file_name_without_extension(file_path):
        f = os.path.split(file_path)[-1]
        return ".".join(f.split(".")[:-1])

    @staticmethod
    def get_relative_directory_path(host_specific_dir_path, full_file_path):
        root_dir = host_specific_dir_path.rstrip("\\")
        file_dir_path = os.path.dirname(full_file_path)
        return file_dir_path[len(root_dir):]

    @staticmethod
    def convert_windows_path_to_unix(windows_path):
        p = windows_path
        p = p.replace("\\", "/")
        if "/" not in p:
            p += "/"
        while p[0] != "/":
            p = p[1:]
        return p

    @staticmethod
    def convert_unix_path_to_windows(unix_path):
        return unix_path.replace("/", "\\")

    @staticmethod
    def convert_file_path_to_environment_standard(file_path):
        if FilePathHelper.is_windows():
            return FilePathHelper.convert_unix_path_to_windows(file_path)
        return FilePathHelper.convert_windows_path_to_unix(file_path)

    @staticmethod
    def is_windows():
        return "win" in sys.platform.lower()

    @staticmethod
    def join(left, right):
        return os.path.join(left, right)