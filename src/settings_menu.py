from tkinter import filedialog
from tkinter.ttk import Labelframe, Button, Label


class SettingsMenu(Labelframe):
    def __init__(self, *args, **kwargs):
        super(SettingsMenu, self).__init__(*args, **kwargs)
        self.outputVideoPath = 'out.mp4'

        self.lbl1 = Label(self, text='Output file:')
        self.lbl1.grid(row=0, column=0)
        self.lblOutputRecording = Label(self, text='out.mp4')
        self.lblOutputRecording.grid(row=0, column=1)
        self.btnBrowse = Button(self, text='Browse', command=self.on_browse)
        self.btnBrowse.grid(row=0, column=2)

        self.btnStartCamera = Button(self, text='Start Camera')
        self.btnStartCamera.grid(row=1, column=2)

    def on_browse(self):
        filename = filedialog.asksaveasfilename(title="Choose recording name",
                                                initialdir=".",
                                                defaultextension=".mp4",
                                                filetypes=[('MPEG', '.mp4'), ('AVI', '.avi')])
        if filename is not None:
            self.outputVideoPath = filename
            self.lblOutputRecording["text"] = filename
