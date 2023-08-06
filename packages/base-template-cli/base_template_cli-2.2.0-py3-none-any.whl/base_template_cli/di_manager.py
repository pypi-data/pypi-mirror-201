from .applyer import Applyer
from .base_template_updater import BaseTemplateUpdater
from .file_copy_util import FileCopyUtil


class DIManager:
    def __init__(
            self,
            dst_root_path,
            base_template_root_path,
            target_dirs,
            only_root,
            lang):
        self.BaseTemplateUpdater = BaseTemplateUpdater(
            base_template_root_path)
        self.FileCopyUtil = FileCopyUtil(
            dst_root_path, base_template_root_path)
        self.Applyer = Applyer(
            self.BaseTemplateUpdater,
            self.FileCopyUtil,
            dst_root_path,
            base_template_root_path,
            target_dirs,
            only_root,
            lang)

    def getInstance(self, classname):
        return getattr(self, classname)
