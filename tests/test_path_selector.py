import unittest
import tkinter as tk
from app.widgets.book_path_selector import create_book_path_selector

class TestBookPathSelector(unittest.TestCase):
    def test_default_path(self):
        root = tk.Tk()
        def dummy_callback(path): pass
        frame, path_var = create_book_path_selector(root, dummy_callback)
        self.assertEqual(path_var.get(), "./books")
        root.destroy()