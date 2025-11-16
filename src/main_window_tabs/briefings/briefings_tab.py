from main_window_tabs.base_tab_widget import BaseTabWidget
from main_window_tabs.base_layout import BaseLayout


class BriefingsTab(BaseTabWidget):
    def __init__(self, layouts: dict[str, BaseLayout]):
        super().__init__()

        self.set_layouts(layouts)
        self.setup_ui()
