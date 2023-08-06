import os
import subprocess


class BaseTemplateUpdater:
    def __init__(self, base_template_path):
        self.original_wd = os.getcwd()
        self.base_template_path = base_template_path
        self.stashed = False
        self.branch = 'main'

    def update(self):
        self.original_wd = os.getcwd()
        os.chdir(self.base_template_path)

        stash_result = subprocess.run(
            ['git', 'stash', '--include-untracked'],
            capture_output=True,
            text=True)
        stash_output = stash_result.stdout.strip()

        if ('no local changes to save' not in stash_output.lower()):
            self.stashed = True

        branch_result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True)
        self.branch = branch_result.stdout.strip()
        subprocess.run(['git', 'switch', 'main'], capture_output=True)
        subprocess.run(['git', 'pull'], capture_output=True)

        os.chdir(self.original_wd)

    def revert(self):
        os.chdir(self.base_template_path)

        subprocess.run(['git', 'switch', self.branch], capture_output=True)

        if not (self.stashed):
            return

        subprocess.run(['git', 'stash', 'pop'], capture_output=True)

        os.chdir(self.original_wd)
