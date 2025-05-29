from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from cryptography.fernet import Fernet

class PasswordBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

        self.site_input = TextInput(hint_text="Website", multiline=False)
        self.user_input = TextInput(hint_text="Username", multiline=False)
        self.pass_input = TextInput(hint_text="Password", multiline=False, password=True)

        self.result_label = Label(text='')

        save_btn = Button(text="Encrypt & Save Password")
        save_btn.bind(on_press=self.save_password)

        self.add_widget(self.site_input)
        self.add_widget(self.user_input)
        self.add_widget(self.pass_input)
        self.add_widget(save_btn)
        self.add_widget(self.result_label)

    def save_password(self, instance):
        site = self.site_input.text
        user = self.user_input.text
        passwd = self.pass_input.text

        if not (site and user and passwd):
            self.result_label.text = "Please fill in all fields!"
            return

        encrypted = self.cipher.encrypt(passwd.encode()).decode()
        with open("passwords.txt", "a", encoding="utf-8") as file:
            file.write(f"{site} | {user} | {encrypted}\n")

        self.result_label.text = "Password saved (encrypted)!"

class PasswordManagerApp(App):
    def build(self):
        return PasswordBox()

if __name__ == '__main__':
    PasswordManagerApp().run()
