from tkinter import Label, Spinbox, Checkbutton, IntVar, OptionMenu, StringVar
from tkinter.ttk import Labelframe


class AlgorithmParameters(Labelframe):
    def __init__(self, algorithms=None, *args, **kwargs):
        super(AlgorithmParameters, self).__init__(*args, **kwargs)
        if algorithms is None:
            algorithms = {}
        self.algorithms = algorithms

        self.lbl1 = Label(self, text='Background Subtraction Algorithm')
        self.lbl1.grid(row=0, column=0)

        keys = list(self.algorithms.keys())
        variable = StringVar(self)
        variable.set(keys[0])
        self.currentAlgorithm = keys[0]
        self.bsaMenu = OptionMenu(self, variable, *keys, command=self.on_algorithm_changed)
        self.bsaMenu.grid(row=0, column=1)

        self.lbl2 = Label(self, text='Median Blur Kernel')
        self.lbl2.grid(row=1, column=0)
        values = [i for i in range(1, 99, 2)]
        values.insert(0, 0)
        self.medianBlurKernel = Spinbox(self, bd=3, values=values)
        self.medianBlurKernel.grid(row=1, column=1)

        self.lbl3 = Label(self, text='Opening Kernel')
        self.lbl3.grid(row=2, column=0)
        self.openKernel = Spinbox(self, bd=3, values=values)
        self.openKernel.grid(row=2, column=1)

        self.lbl4 = Label(self, text='Inverse Binary')
        self.lbl4.grid(row=3, column=0)
        self.inverseBinaryVariable = IntVar()
        self.inverseBinaryCheckbutton = Checkbutton(self, text="Enable", variable=self.inverseBinaryVariable)
        self.inverseBinaryCheckbutton.grid(row=3, column=1)

        var_contour = StringVar(self)
        var_contour.set("200")
        self.lbl5 = Label(self, text='Contour Threshold')
        self.lbl5.grid(row=4, column=0)
        self.contourThreshold = Spinbox(self, bd=3, from_=0, to=99999, textvariable=var_contour)
        self.contourThreshold.grid(row=4, column=1)

    def on_algorithm_changed(self, algorithm):
        self.currentAlgorithm = algorithm
