from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
from kivy.app import App

# 🎨 Theme Colors (adjust if needed)
PRIMARY_BLUE = (0.2, 0.6, 0.86, 1)   # Main accent
GRAY_TEXT = (0.5, 0.5, 0.5, 1)       # Subtle labels
DARK_TEXT = (0.1, 0.1, 0.1, 1)       # Main text
LIGHT_TEXT = (0.9, 0.9, 0.9, 1)      # Light text for dark theme
CARD_BG = (0.95, 0.95, 0.97, 1)      # Light gray for cards
DARK_THEME_BG = (0.15, 0.15, 0.15, 1) # Dark background for dark theme
DARK_CARD_BG = (0.2, 0.2, 0.2, 1)    # Dark gray for cards in dark theme


# 🏷️ Custom Label
class DWLabel(Label):
    def __init__(self, **kwargs):
        kwargs.setdefault("color", DARK_TEXT)
        kwargs.setdefault("font_size", "16sp")
        super().__init__(**kwargs)
        self.default_color = kwargs.get("color", DARK_TEXT)
        self.bind(on_kv_post=self.on_post_init)

    def on_post_init(self, instance, value):
        app = App.get_running_app()
        if hasattr(app, 'theme_manager'):
            app.theme_manager.bind(is_dark_theme=self.on_theme_change)

    def on_theme_change(self, instance, is_dark_theme):
        if is_dark_theme:
            self.color = LIGHT_TEXT
        else:
            self.color = self.default_color


# 🔘 Custom Button
class DWButton(Button):
    def __init__(self, **kwargs):
        kwargs.setdefault("background_normal", "")
        kwargs.setdefault("background_color", PRIMARY_BLUE)
        kwargs.setdefault("color", (1, 1, 1, 1))
        kwargs.setdefault("font_size", "16sp")
        kwargs.setdefault("size_hint", (None, None))
        kwargs.setdefault("height", dp(45))
        super().__init__(**kwargs)
        self.default_background_color = kwargs.get("background_color", PRIMARY_BLUE)
        self.primary = kwargs.get("primary", False)  # ✅ define primary flag safely
        self.bind(on_kv_post=self.on_post_init)

    def on_post_init(self, instance, value):
        app = App.get_running_app()
        if hasattr(app, 'theme_manager'):
            app.theme_manager.bind(is_dark_theme=self.on_theme_change)

    def on_theme_change(self, instance, is_dark_theme):
        if is_dark_theme:
            if self.primary:
                self.background_color = PRIMARY_BLUE
                self.color = (1, 1, 1, 1)
            else:
                self.background_color = DARK_CARD_BG
                self.color = LIGHT_TEXT
        else:
            self.background_color = self.default_background_color
            if not self.primary:
                self.color = DARK_TEXT
            else:
                self.color = (1, 1, 1, 1)


# 📦 Flat Card Container (modern look)
class DWCard(BoxLayout):
    def __init__(self, **kwargs):
        kwargs.setdefault("orientation", "vertical")
        kwargs.setdefault("padding", dp(12))
        kwargs.setdefault("spacing", dp(8))
        super().__init__(**kwargs)

        with self.canvas.before:
            self.bg_color = Color(*CARD_BG)
            self.rect = RoundedRectangle(
                radius=[dp(16)],
                pos=self.pos,
                size=self.size
            )
        self.bind(pos=self._update_rect, size=self._update_rect)
        self.bind(on_kv_post=self.on_post_init)

    def on_post_init(self, instance, value):
        app = App.get_running_app()
        if hasattr(app, 'theme_manager'):
            app.theme_manager.bind(is_dark_theme=self.on_theme_change)

    def on_theme_change(self, instance, is_dark_theme):
        if is_dark_theme:
            self.bg_color.rgba = DARK_CARD_BG
        else:
            self.bg_color.rgba = CARD_BG

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


# 📱 App Item Row (icon + labels + usage bar)
class DWAppItem(BoxLayout):
    def __init__(self, app_name, icon_path, usage_minutes, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(60)
        self.spacing = dp(10)
        self.padding = [dp(8), dp(4)]

        # App Icon
        self.add_widget(Image(source=icon_path, size_hint=(None, None), size=(dp(40), dp(40))))

        # App name + usage text stacked vertically
        text_box = BoxLayout(orientation="vertical", spacing=dp(2))
        self.app_name_label = Label(text=app_name, color=DARK_TEXT, bold=True, halign="left", valign="middle")
        self.usage_label = Label(text=f"{usage_minutes} min", font_size="12sp", color=GRAY_TEXT, halign="left")
        text_box.add_widget(self.app_name_label)
        text_box.add_widget(self.usage_label)
        self.add_widget(text_box)

        # Usage Progress Bar
        self.usage_bar = ProgressBar(max=120, value=usage_minutes, size_hint=(0.4, None), height=dp(12))
        self.add_widget(self.usage_bar)

        self.bind(on_kv_post=self.on_post_init)

    def on_post_init(self, instance, value):
        app = App.get_running_app()
        if hasattr(app, 'theme_manager'):
            app.theme_manager.bind(is_dark_theme=self.on_theme_change)

    def on_theme_change(self, instance, is_dark_theme):
        if is_dark_theme:
            self.app_name_label.color = LIGHT_TEXT
            self.usage_label.color = LIGHT_TEXT
            self.usage_bar.background_color = DARK_THEME_BG
            self.usage_bar.foreground_color = PRIMARY_BLUE
        else:
            self.app_name_label.color = DARK_TEXT
            self.usage_label.color = GRAY_TEXT
            self.usage_bar.background_color = [0, 0, 0, 0]  # reset
            self.usage_bar.foreground_color = [0, 0, 0, 0]  # reset
