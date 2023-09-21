from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class TrainingsScreen(Screen):
    training_positions = {}

    def on_enter(self):
        self.update_trainings_list()

    def add_training(self):
        new_training = self.ids.new_training_input.text
        if new_training:
            self.training_positions[new_training] = None  # Initialize the time to None
            self.ids.new_training_input.text = ""  # Clear the input field after adding
            self.update_trainings_list()

    def remove_training(self, training_name):
        if training_name in self.training_positions:
            del self.training_positions[training_name]
            self.update_trainings_list()

    def update_trainings_list(self):
        trainings_scrollview = self.ids.trainings_scrollview
        trainings_scrollview.clear_widgets()

        trainings_layout = BoxLayout(orientation='vertical', spacing='5dp', size_hint_y=None)
        trainings_layout.bind(minimum_height=trainings_layout.setter('height'))
        for training, time in self.training_positions.items():
            entry_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='30dp')
            edit_button = Button(
                text="Edit", size_hint_x=0.1, size_hint_y=None, height='30dp', font_size='16sp'
            )
            edit_button.bind(on_release=lambda btn, training_name=training: self.edit_training(training_name))

            training_label = Label(
                text=f"{training}", size_hint_x=0.7, height='30dp', font_size='18sp'
            )


            delete_button = Button(
                text="x", size_hint_x=0.05, size_hint_y=None, height='30dp', font_size='16sp'
            )
            delete_button.bind(on_release=lambda btn, training_name=training: self.remove_training(training_name))

            entry_layout.add_widget(edit_button)
            entry_layout.add_widget(training_label)
            entry_layout.add_widget(delete_button)

            trainings_layout.add_widget(entry_layout)

        trainings_scrollview.add_widget(trainings_layout)

    def edit_training(self, training_name):
        edit_screen = self.manager.get_screen('edit_training')
        edit_screen.set_training(self, training_name)
        self.manager.current = 'edit_training'