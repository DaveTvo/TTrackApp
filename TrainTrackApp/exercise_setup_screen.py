from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput


class ExerciseSetupScreen(Screen):
    spinner_value = StringProperty()

    def __init__(self, **kwargs):
        super(ExerciseSetupScreen, self).__init__(**kwargs)
        self.ids.exercise_type_spinner.bind(text=self.on_spinner_change)
        self.on_spinner_value(None, self.ids.series_number_spinner.text)

    def on_spinner_value(self, instance, value):
        # Get the current non-empty series inputs
        non_empty_inputs = [input for input in self.ids.series_inputs.children if input.text]

        # If the new value is less than the number of non-empty inputs, set it to the max value
        if int(value) < len(non_empty_inputs):
            self.ids.series_number_spinner.text = str(len(non_empty_inputs))
            self.ids.message_label.text = f"{len(non_empty_inputs)} inputs fulfilled.\n" \
                                          f"To decrease Amount of Series more\n" \
                                          f"remove some of them"
            return

        # Remove existing series inputs and save their values
        series_values = [input.text for input in self.ids.series_inputs.children]
        self.ids.series_inputs.clear_widgets()

        # Get unit type from spinner text
        unit_type = self.ids.exercise_type_spinner.text.split('[')[1].split(']')[0]

        # Create new series inputs and apply the saved values if available
        for i in range(1, int(value) + 1):
            new_input = self.create_series_input(unit_type)
            try:
                new_input.text = series_values[-i]
            except IndexError:
                pass
            self.ids.series_inputs.add_widget(new_input)

        # If the spinner value is not less than the number of non-empty inputs, clear the message
        self.ids.message_label.text = ""

    def on_spinner_change(self, instance, value):
        # Get unit type from spinner text
        unit_type = value.split('[')[1].split(']')[0]

        # Update series inputs hint_text
        for child in self.ids.series_inputs.children:
            child.hint_text = unit_type

    @staticmethod
    def create_series_input(unit_type):
        new_input = TextInput()
        new_input.size_hint = None, None
        new_input.height = '30dp'
        new_input.multiline = False
        new_input.hint_text = f"{unit_type}"
        new_input.bind(text=ExerciseSetupScreen.validate_text)
        return new_input

    def get_unit_type(self):
        # Get unit type from spinner text
        return self.ids.exercise_type_spinner.text.split('[')[1].split(']')[0]

    def on_enter(self):
        self.ids.series_number_spinner.bind(text=self.on_spinner_value)

    def on_leave(self):
        self.ids.series_number_spinner.unbind(text=self.on_spinner_value)

    def save_exercise(self):
        edit_training_screen = self.manager.get_screen('edit_training')
        edit_training_screen.update_exercise_name(self.ids.exercise_name_input.text)

    @staticmethod
    def validate_text(instance, value):
        try:
            # Only allow float values
            float(value)
            # Check for two or fewer decimal places
            if len(value.split('.')[-1]) > 2:
                raise ValueError
        except ValueError:
            # If the input is not a valid float or has more than two decimal places, remove the last character
            instance.text = instance.text[:-1]
