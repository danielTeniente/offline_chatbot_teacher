import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from app.widgets.book_path_selector import create_book_path_selector, DEFAULT_PATH

class TestBookPathSelector(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window during tests

    def tearDown(self):
        self.root.destroy()

    def test_default_path(self):
        def dummy_callback(path): pass
        frame, path_var = create_book_path_selector(self.root, dummy_callback)
        self.assertEqual(path_var.get(), DEFAULT_PATH)

    @patch('app.widgets.book_path_selector.filedialog.askdirectory')
    def test_select_folder_updates_path_and_calls_callback(self, mock_askdirectory):
        mock_askdirectory.return_value = "/new/path"
        callback_called = False
        selected_path = None

        def dummy_callback(path):
            nonlocal callback_called, selected_path
            callback_called = True
            selected_path = path

        frame, path_var = create_book_path_selector(self.root, dummy_callback)

        # Simulate button click
        for child in frame.winfo_children():
            if isinstance(child, tk.Button) and child['text'] == 'Cambiar':
                child.invoke()
                break

        self.assertEqual(path_var.get(), "/new/path")
        self.assertTrue(callback_called)
        self.assertEqual(selected_path, "/new/path")

    @patch('app.widgets.book_path_selector.filedialog.askdirectory')
    def test_select_folder_cancel_does_not_change_path(self, mock_askdirectory):
        mock_askdirectory.return_value = ""  # Simulate cancel
        callback_called = False

        def dummy_callback(path):
            nonlocal callback_called
            callback_called = True

        frame, path_var = create_book_path_selector(self.root, dummy_callback)

        # Simulate button click
        for child in frame.winfo_children():
            if isinstance(child, tk.Button) and child['text'] == 'Cambiar':
                child.invoke()
                break

        self.assertEqual(path_var.get(), DEFAULT_PATH)
        self.assertFalse(callback_called)