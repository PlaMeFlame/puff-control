import os
import json
from datetime import date

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout

# KV Layout definition with dark theme and vibrant neon accents
KV = '''
<MainScreen>:
    md_bg_color: self.bg_color

    MDBoxLayout:
        orientation: 'vertical'
        spacing: "12dp"

        # Top Bar
        MDTopAppBar:
            title: "Puff Control"
            elevation: 4
            md_bg_color: 0.12, 0.14, 0.18, 1
            specific_text_color: 0.0, 1.0, 0.53, 1
            right_action_items: [["cog", lambda x: app.open_settings_dialog()]]

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: ["20dp", "16dp", "20dp", "20dp"]
                spacing: "24dp"
                adaptive_height: True

                # Progress & Counter Card
                MDCard:
                    orientation: 'vertical'
                    padding: "20dp"
                    spacing: "16dp"
                    radius: [20, 20, 20, 20]
                    md_bg_color: root.card_bg_color
                    elevation: 3
                    adaptive_height: True

                    MDLabel:
                        text: "СУТОЧНАЯ СТАТИСТИКА"
                        font_style: "Caption"
                        theme_text_color: "Custom"
                        text_color: 0.7, 0.7, 0.75, 1
                        halign: "center"
                        bold: True

                    MDLabel:
                        text: f"Затяжек сегодня: {root.current_puffs} / {root.daily_limit}"
                        font_style: "H5"
                        theme_text_color: "Custom"
                        text_color: root.accent_color
                        halign: "center"
                        bold: True

                    MDProgressBar:
                        value: root.progress_percent
                        color: root.accent_color
                        height: "10dp"

                    MDLabel:
                        text: root.status_message
                        font_style: "Subtitle2"
                        theme_text_color: "Custom"
                        text_color: root.status_text_color
                        halign: "center"
                        bold: True

                # Main Action Section
                MDBoxLayout:
                    orientation: 'vertical'
                    alignment: ['center', 'center']
                    spacing: "16dp"
                    adaptive_height: True
                    padding: ["0dp", "20dp", "0dp", "20dp"]

                    MDRaisedButton:
                        id: puff_btn
                        text: root.button_text
                        font_size: "20sp"
                        bold: True
                        size_hint: (None, None)
                        size: ("240dp", "80dp")
                        radius: [40, 40, 40, 40]
                        md_bg_color: root.button_bg_color
                        text_color: root.button_text_color
                        elevation: 6
                        disabled: root.button_disabled
                        on_release: root.on_puff_pressed()

                # Extra Information Cards
                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: "12dp"
                    adaptive_height: True

                    MDCard:
                        orientation: 'vertical'
                        padding: "14dp"
                        spacing: "4dp"
                        radius: [16, 16, 16, 16]
                        md_bg_color: 0.12, 0.14, 0.18, 1
                        size_hint_x: 0.5
                        adaptive_height: True

                        MDLabel:
                            text: "Осталось"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: 0.6, 0.6, 0.65, 1
                            halign: "center"

                        MDLabel:
                            text: f"{max(0, root.daily_limit - root.current_puffs)}"
                            font_style: "H6"
                            theme_text_color: "Custom"
                            text_color: 0.0, 0.9, 1.0, 1
                            halign: "center"
                            bold: True

                    MDCard:
                        orientation: 'vertical'
                        padding: "14dp"
                        spacing: "4dp"
                        radius: [16, 16, 16, 16]
                        md_bg_color: 0.12, 0.14, 0.18, 1
                        size_hint_x: 0.5
                        adaptive_height: True

                        MDLabel:
                            text: "Отдых"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: 0.6, 0.6, 0.65, 1
                            halign: "center"

                        MDLabel:
                            text: f"{root.cooldown_time} сек."
                            font_style: "H6"
                            theme_text_color: "Custom"
                            text_color: 0.0, 0.9, 1.0, 1
                            halign: "center"
                            bold: True

<SettingsContent>:
    orientation: 'vertical'
    spacing: "16dp"
    size_hint_y: None
    height: "180dp"

    MDTextField:
        id: limit_field
        hint_text: "Суточный лимит затяжек"
        text: str(root.limit_val)
        input_filter: "int"
        mode: "rectangle"

    MDTextField:
        id: cooldown_field
        hint_text: "Таймер отдыха (в секундах)"
        text: str(root.cooldown_val)
        input_filter: "int"
        mode: "rectangle"

    MDRaisedButton:
        text: "Сбросить счетчик за сегодня"
        md_bg_color: 0.85, 0.2, 0.2, 1
        text_color: 1, 1, 1, 1
        size_hint_x: 1
        on_release: app.reset_today_counter()
'''

class SettingsContent(MDBoxLayout):
    limit_val = NumericProperty(50)
    cooldown_val = NumericProperty(30)


class MainScreen(MDScreen):
    current_puffs = NumericProperty(0)
    daily_limit = NumericProperty(50)
    cooldown_time = NumericProperty(30)
    
    cooldown_remaining = NumericProperty(0)
    button_disabled = BooleanProperty(False)
    
    progress_percent = NumericProperty(0)
    status_message = StringProperty("Готов к работе")
    button_text = StringProperty("СДЕЛАТЬ ЗАТЯЖКУ")
    
    # Theme colors
    bg_color = ListProperty([0.07, 0.08, 0.11, 1])          # Dark background #12141C
    card_bg_color = ListProperty([0.12, 0.14, 0.18, 1])    # Dark slate card
    accent_color = ListProperty([0.0, 1.0, 0.53, 1])        # Neon Green #00FF87
    status_text_color = ListProperty([0.0, 1.0, 0.53, 1])
    
    button_bg_color = ListProperty([0.0, 1.0, 0.53, 1])
    button_text_color = ListProperty([0.05, 0.05, 0.08, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cooldown_event = None

    def update_ui_state(self):
        """Update progress bar, labels, colors, and button state based on limits and cooldown."""
        # Calculate progress percent
        if self.daily_limit > 0:
            self.progress_percent = min(100.0, (self.current_puffs / float(self.daily_limit)) * 100.0)
        else:
            self.progress_percent = 100.0

        # Check if daily limit reached
        if self.current_puffs >= self.daily_limit:
            self.button_disabled = True
            self.button_text = "ЛИМИТ ИСЧЕРПАН"
            self.status_message = "⚠️ Лимит на сегодня исчерпан!"
            self.status_text_color = [1.0, 0.2, 0.35, 1]  # Bright Red
            self.accent_color = [1.0, 0.2, 0.35, 1]
            self.card_bg_color = [0.22, 0.10, 0.12, 1]    # Reddish tint card background
            self.button_bg_color = [0.35, 0.15, 0.18, 1]
            self.button_text_color = [0.7, 0.5, 0.5, 1]
        elif self.cooldown_remaining > 0:
            self.button_disabled = True
            self.button_text = f"ОТДЫХ ({self.cooldown_remaining}s)"
            self.status_message = f"Пауза между затяжками: {self.cooldown_remaining} сек."
            self.status_text_color = [1.0, 0.75, 0.0, 1]  # Neon Amber
            self.accent_color = [0.0, 1.0, 0.53, 1]
            self.card_bg_color = [0.12, 0.14, 0.18, 1]
            self.button_bg_color = [0.2, 0.25, 0.3, 1]
            self.button_text_color = [0.6, 0.6, 0.6, 1]
        else:
            self.button_disabled = False
            self.button_text = "СДЕЛАТЬ ЗАТЯЖКУ"
            self.status_message = "Отлично! Пауза выдержана."
            self.status_text_color = [0.0, 1.0, 0.53, 1]
            self.accent_color = [0.0, 1.0, 0.53, 1]
            self.card_bg_color = [0.12, 0.14, 0.18, 1]
            self.button_bg_color = [0.0, 1.0, 0.53, 1]
            self.button_text_color = [0.05, 0.05, 0.08, 1]

    def on_puff_pressed(self):
        """Handle puff button press event."""
        if self.current_puffs < self.daily_limit and self.cooldown_remaining <= 0:
            self.current_puffs += 1
            app = MDApp.get_running_app()
            app.vibrate_device(120)
            app.save_data()

            if self.current_puffs < self.daily_limit:
                self.start_cooldown()
            else:
                self.update_ui_state()

    def start_cooldown(self):
        """Start countdown timer for rest period."""
        self.cooldown_remaining = self.cooldown_time
        self.update_ui_state()
        if self.cooldown_event:
            self.cooldown_event.cancel()
        self.cooldown_event = Clock.schedule_interval(self.tick_cooldown, 1)

    def tick_cooldown(self, dt):
        """Per-second cooldown timer tick."""
        self.cooldown_remaining -= 1
        if self.cooldown_remaining <= 0:
            self.cooldown_remaining = 0
            if self.cooldown_event:
                self.cooldown_event.cancel()
                self.cooldown_event = None
        self.update_ui_state()


class PuffControlApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.storage_file = os.path.join(self.user_data_dir, "puff_store.json")
        
        Builder.load_string(KV)
        self.main_screen = MainScreen()
        self.load_data()
        return self.main_screen

    def load_data(self):
        """Load stored app state or set default values with auto-reset on new day."""
        today_str = date.today().isoformat()
        
        data = {
            "date": today_str,
            "current_puffs": 0,
            "daily_limit": 50,
            "cooldown_time": 30
        }

        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    saved_data = json.load(f)
                    data.update(saved_data)
            except Exception as e:
                print(f"Error loading storage: {e}")

        # Check for new day reset
        if data.get("date") != today_str:
            data["current_puffs"] = 0
            data["date"] = today_str

        self.main_screen.daily_limit = int(data.get("daily_limit", 50))
        self.main_screen.cooldown_time = int(data.get("cooldown_time", 30))
        self.main_screen.current_puffs = int(data.get("current_puffs", 0))
        self.main_screen.update_ui_state()
        self.save_data()

    def save_data(self):
        """Persist current state to local JSON file."""
        data = {
            "date": date.today().isoformat(),
            "current_puffs": self.main_screen.current_puffs,
            "daily_limit": self.main_screen.daily_limit,
            "cooldown_time": self.main_screen.cooldown_time
        }
        try:
            os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving storage: {e}")

    def vibrate_device(self, duration_ms=100):
        """Vibrate device on Android platform."""
        if platform == 'android':
            try:
                from plyer import vibrator
                vibrator.vibrate(time=duration_ms / 1000.0)
            except Exception:
                try:
                    from jnius import autoclass
                    PythonActivity = autoclass('org.kivy.android.PythonActivity')
                    Context = autoclass('android.content.Context')
                    activity = PythonActivity.mActivity
                    vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)
                    if vibrator and vibrator.hasVibrator():
                        vibrator.vibrate(duration_ms)
                except Exception as e:
                    print(f"Vibration warning: {e}")

    def open_settings_dialog(self):
        """Open popup dialog to configure daily limit and cooldown timer."""
        self.settings_content = SettingsContent(
            limit_val=self.main_screen.daily_limit,
            cooldown_val=self.main_screen.cooldown_time
        )
        
        self.dialog = MDDialog(
            title="Настройки Puff Control",
            type="custom",
            content_cls=self.settings_content,
            buttons=[
                MDFlatButton(
                    text="ОТМЕНА",
                    theme_text_color="Custom",
                    text_color=[0.7, 0.7, 0.7, 1],
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="СОХРАНИТЬ",
                    md_bg_color=[0.0, 0.8, 0.4, 1],
                    on_release=lambda x: self.save_settings_from_dialog()
                ),
            ],
        )
        self.dialog.open()

    def save_settings_from_dialog(self):
        """Read text fields from dialog and apply new settings."""
        if not self.dialog or not self.settings_content:
            return
            
        try:
            new_limit = int(self.settings_content.ids.limit_field.text.strip())
            new_cooldown = int(self.settings_content.ids.cooldown_field.text.strip())
            
            if new_limit > 0 and new_cooldown >= 0:
                self.main_screen.daily_limit = new_limit
                self.main_screen.cooldown_time = new_cooldown
                self.main_screen.update_ui_state()
                self.save_data()
        except ValueError:
            pass

        self.dialog.dismiss()

    def reset_today_counter(self):
        """Manual reset of today's puff counter."""
        self.main_screen.current_puffs = 0
        if self.main_screen.cooldown_event:
            self.main_screen.cooldown_event.cancel()
            self.main_screen.cooldown_event = None
        self.main_screen.cooldown_remaining = 0
        self.main_screen.update_ui_state()
        self.save_data()
        if self.dialog:
            self.dialog.dismiss()


if __name__ == '__main__':
    PuffControlApp().run()
