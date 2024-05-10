import tkinter as tk


class Keypad(tk.Frame):
    """A keypad widget for tkinter"""

    def __init__(self, parent, keynames=[], label="", columns=1,
                 radio=False, **kwargs):
        super().__init__(parent, kwargs)
        self.keynames = keynames
        if radio:
            self.var = tk.IntVar()
        self.init_components(columns, label, radio)

    @property
    def frame(self):
        """Getter for the keypad's frame"""
        return super()

    def init_components(self, columns, label, radio) -> None:
        """Create a keypad of keys using the keynames list.
        The first keyname is at the top left of the keypad and
        fills the available columns left-to-right, adding as many
        rows as needed.
        :param columns: number of columns to use
        :param label: A label for the keypad
        :param radio: Determines whether the keypad uses regular buttons
                      or Radio buttons
        """
        settings = {"padx": 2, "pady": 2, "sticky": tk.NSEW}
        if label:
            key_label = tk.Label(self, text=label)
            key_label.grid(column=0, row=0, sticky=tk.N)
        column = 0
        row = columns
        if radio:
            for key in self.keynames:
                button = tk.Radiobutton(self, text=key, variable=self.var,
                                        value=column, indicatoron=False)
                button.grid(column=column % columns, row=row // columns,
                            **settings)
                self.rowconfigure(row // columns, weight=1)
                self.columnconfigure(column % columns, weight=1)
                column += 1
                row += 1
        else:
            for key in self.keynames:
                button = tk.Button(self, text=key)
                button.grid(column=column % columns, row=row // columns,
                            **settings)
                self.rowconfigure(row // columns, weight=1)
                self.columnconfigure(column % columns, weight=1)
                column += 1
                row += 1

    def bind(self, sequence, func, add=''):
        """Bind an event handler to an event sequence."""
        for button in self.children.values():
            button.bind(sequence, func, add)

    def __setitem__(self, key, value) -> None:
        """Overrides __setitem__ to allow configuration of all buttons
        using dictionary syntax.

        Example: keypad['foreground'] = 'red'
        sets the font color on all buttons to red.
        """
        for button in self.children.values():
            button[key] = value

    def __getitem__(self, key):
        """Overrides __getitem__ to allow reading of configuration values
        from buttons.
        Example: keypad['foreground'] would return 'red' if the button
        foreground color is 'red'.
        """
        for button in self.children.values():
            return button.__getitem__(key)

    def configure(self, cnf=None, **kwargs):
        """Apply configuration settings to all buttons.

        To configure properties of the frame that contains the buttons,
        use `keypad.frame.configure()`.
        """
        for button in self.children.values():
            if not isinstance(button, (tk.Button, tk.Radiobutton)):
                pass
            else:
                button.configure(cnf, **kwargs)

    def set_button(self, index, key, value):
        """Configures a specific button in the keypad"""
        if index == 1:
            index = ""
        for button in self.children.keys():
            if button in [f"!button{index}", f"!radiobutton{index}"]:
                self.children[button][key] = value
                return

    def bind_button(self, sequence, function, index, add=''):
        """Binds a specific button to an event"""
        if index == 1:
            index = ""
        for button in self.children.keys():
            if button == f"!button{index}":
                self.children[button].bind(sequence, function, add)
                return

if __name__ == "__main__":
    x = tk.Tk()
    x.title("testing")
    a = Keypad(x, ["1","2","3","4","5","6"], "test", 2)
    a.pack(expand=True, fill="both")
    x.mainloop()