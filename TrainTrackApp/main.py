from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from edit_training_screen import EditTrainingScreen
from exercise_setup_screen import ExerciseSetupScreen
from trainings_screen import TrainingsScreen
from database_handler import DatabaseHandler, TrainingsTable, ExerciseTable
import sqlite3


class MainScreen(Screen):
    pass


class StatisticsScreen(Screen):
    pass


class MyApp(App):
    # training_db = TrainingsTable()
    # TrainingsTable.create_trainings_table(training_db.db_connection)

    def build(self):
        # training_name = "Morning Workout"
        # training_time = 60  # in minutes
        # self.training_db.add_training(training_name, training_time)
        # print("Trainings:")
        # self.training_db.select_from_table("trainings")
        #
        # self.training_db.close_db_connection()
        self.screen_manager = ScreenManager()

        self.screen_manager.add_widget(MainScreen(name='main'))
        self.screen_manager.add_widget(TrainingsScreen(name='trainings'))
        self.screen_manager.add_widget(StatisticsScreen(name='statistics'))
        self.screen_manager.add_widget(EditTrainingScreen(name='edit_training'))
        self.screen_manager.add_widget(ExerciseSetupScreen(name='exercise_setup'))

        return self.screen_manager


if __name__ == '__main__':
    MyApp().run()
