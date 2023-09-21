from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class EditTrainingScreen(Screen):
    training_name = ""
    exercises = {}
    current_exercise = ""

    def __init__(self, **kwargs):
        super(EditTrainingScreen, self).__init__(**kwargs)
        self.trainings_screen_ref = None

    def set_training(self, trainings_screen, training_name):
        self.trainings_screen_ref = trainings_screen
        self.training_name = training_name
        self.ids.training_name_input.text = training_name  # Set the TextInput to the current training name

    def save_edit(self):
        # Get the new training name from the training_name_input TextInput
        new_training_name = self.ids.training_name_input.text

        # Get the time entered in the edit_input TextInput
        time_input = self.ids.edit_input.text
        time_minutes = int(time_input) if time_input else None

        # Update the training name and time in TrainingsScreen
        if self.trainings_screen_ref:
            if new_training_name != self.training_name:
                # If the training name has changed, update the key in the dictionary
                self.trainings_screen_ref.training_positions[new_training_name] = self.trainings_screen_ref.training_positions.pop(self.training_name)
                self.training_name = new_training_name

            self.trainings_screen_ref.training_positions[self.training_name] = time_minutes
            self.trainings_screen_ref.update_trainings_list()  # Update the TrainingsScreen list

    def add_exercise(self):
        new_exercise = self.ids.new_exercise_input.text
        if new_exercise:
            self.exercises[new_exercise] = None  # Initialize the time to None
            self.ids.new_exercise_input.text = ""  # Clear the input field after adding
            self.update_exercises_list()

    def edit_exercise(self, exercise_name):
        exercise_screen = self.manager.get_screen('exercise_setup')
        exercise_screen.ids.exercise_name_input.text = exercise_name  # Set the TextInput to the current exercise name
        self.current_exercise = exercise_name  # Set the current exercise to the exercise being edited
        self.manager.current = 'exercise_setup'

    def remove_exercise(self, exercise_name):
        if exercise_name in self.exercises:
            del self.exercises[exercise_name]
            self.update_exercises_list()

    def update_exercises_list(self):
        exercises_scrollview = self.ids.exercises_scrollview
        exercises_scrollview.clear_widgets()

        exercises_layout = BoxLayout(orientation='vertical', spacing='5dp', size_hint_y=None)
        exercises_layout.bind(minimum_height=exercises_layout.setter('height'))
        for exercise, time in self.exercises.items():
            entry_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='30dp')
            edit_button = Button(
                text="Edit", size_hint_x=0.1, size_hint_y=None, height='30dp', font_size='16sp'
            )
            edit_button.bind(on_release=lambda btn, exercise_name=exercise: self.edit_exercise(exercise_name))

            exercise_label = Label(
                text=f"{exercise}", size_hint_x=0.7, height='30dp', font_size='18sp'
            )

            delete_button = Button(
                text="x", size_hint_x=0.05, size_hint_y=None, height='30dp', font_size='16sp'
            )
            delete_button.bind(on_release=lambda btn, exercise_name=exercise: self.remove_exercise(exercise_name))

            entry_layout.add_widget(edit_button)
            entry_layout.add_widget(exercise_label)
            entry_layout.add_widget(delete_button)

            exercises_layout.add_widget(entry_layout)

        exercises_scrollview.add_widget(exercises_layout)

    def update_exercise_name(self, new_exercise_name):
        if new_exercise_name and self.current_exercise in self.exercises:
            self.exercises[new_exercise_name] = self.exercises.pop(self.current_exercise)
            self.update_exercises_list()
