import os
import shutil


class FileCopyUtil:
    def __init__(self, dst_root_path, base_template_root_path):
        self.dst_root_path = dst_root_path
        self.base_template_root_path = base_template_root_path

    def copy_files(self, target_dirs, files):
        ignore_files = ['.DS_Store', 'CHANGELOG.md']

        for file in files:
            if file in ignore_files:
                continue

            shutil.copy(
                os.path.join(self.base_template_root_path, target_dirs, file),
                os.path.join(self.dst_root_path, target_dirs)
            )

    def copy_all_files(self, target_dirs):
        target_dir_path = os.path.join(
            self.base_template_root_path, target_dirs)
        target_files = os.listdir(target_dir_path)
        files = [
            f for f in target_files if os.path.isfile(
                os.path.join(
                    target_dir_path, f))]
        self.copy_files(target_dirs, files)
