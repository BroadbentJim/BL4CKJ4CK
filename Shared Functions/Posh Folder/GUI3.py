import tkinter as tk   # python3
#import tkinter.ttk as ttk
import datetime, os
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


TITLE_FONT = ("Helvetica", 18, "bold")
LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="favicon.ico")
        tk.Tk.wm_title(self, "BL4CKJ4CK")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.shared_data = {
            "strategy": tk.StringVar(),
            "results": {},
            "HRM": np.zeros([18,10]),
            "repeat": tk.BooleanVar(),
        }
        self.shared_data["repeat"].set(True)
        self.frames = {}
        for F in (StartPage, Main_Page, About_Page, Input_Page, GraphPage, Results):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.initUI()
        frame.tkraise()
    # def update_dictionary(self, button, arg):
    #     self.shared_data[button] = arg
    #
    # def get_page(self, page_class):
    #     return self.frames[page_class]


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text=("""BL4CKJ4CK Simulator"""), font=TITLE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="About", command=lambda: controller.show_frame("About_Page"))
        button.pack()

        maintext = tk.Label(self, text=("""This program follows typical casino blackjack rules.
        This means no splitting on non-alike face cards,
        a soft 17 rule and inability to double after splitting.
        The house pays 3:2 on blackjack as per most casinos.
        The program tries to follow casino rules as strictly as
        possible in order to produce results that are comparable
        to the casino."""), font=NORM_FONT)
        maintext.pack(pady=20, padx=10)

        button1 = tk.Button(self, text="Continue",
                             command=lambda: controller.show_frame("Input_Page"))
        button1.pack()

        button2 = tk.Button(self, text="Quit",
                             command=quit)
        button2.pack()
    def initUI(self):
        pass

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

class Input_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="This is the input page", font=TITLE_FONT)
        title.pack(side="top", fill="x", pady=10)



        self.repeatsims = self.controller.shared_data["repeat"]
        self.repeatsims.set(True)
        multiplesims = tk.Checkbutton(self, text="Repeat simulations", variable=self.repeatsims, font=LARGE_FONT)
        multiplesims.pack()

        optionslabel = tk.Label(self, text="Choose your player strategy:", font=LARGE_FONT)
        optionslabel.pack()
        options = ['Basic', 'Perfect', 'Simple', 'Monte Carlo']
        self.strategy = self.controller.shared_data["strategy"]
        self.strategy.set(str(options[0]))
        self.optionmenu = tk.OptionMenu(self, self.strategy, *options, command=lambda x: self.Toggle())
        self.optionmenu.pack()

        self.hittolabel = tk.Label(self, text="What would you like to hit too", font=NORM_FONT)
        self.hittolabel.pack()
        self.hittolabel.lower()
        self.hitto = tk.IntVar()
        self.basicbutton = tk.Entry(self, textvariable=self.hitto)
        self.basicbutton.config(state = tk.DISABLED)
        self.basicbutton.pack(pady=0)

        # if self.strategy.get() == "Basic":
        #     basicbutton.config(state=tk.NORMAL)


        simslabel = tk.Label(self, text="Number of times to simulate:", font=LARGE_FONT)
        simslabel.pack()
        self.numberofsims = tk.IntVar()
        self.numberofsims.set(100)
        self.entrylist = tk.Entry(self, textvariable=self.numberofsims)
        self.entrylist.pack()


        startbutton = tk.Button(self, text="Start simulation", command=self.games)
        startbutton.pack()

    # def startsimulation(self):
    #     if self.strategy.get() == 'Basic':
    #         basic(self.numberofsims.get())
    #     elif self.strategy.get() == 'Simple':
    #         simple(self.numberofsims.get(), self.hitto.get())
    #     elif self.strategy.get() == 'Perfect':
    #         perfect(self.numberofsims.get())
    #     elif self.strategy.get() == 'Monte':
    #         monte(self.numberofsims.get())

    def games(self):
        strategy = self.strategy.get()
        numberofsims = self.numberofsims.get()
        wanted = self.hitto.get()
        repeat = self.repeatsims.get()
        if strategy == "Simple":
            if repeat:
                from SimpleStrategy import simulations as simple
                results = simple(numberofsims, wanted)  # Dictionary
            else:
                from SimpleStrategy import game
                results = game(numberofsims, wanted)
        elif strategy == "Basic":
            if repeat:
                from BasicStrategy import simulations as basic
                results = basic(numberofsims)
            else:
                from BasicStrategy import game
                results = game(numberofsims)
        elif strategy == "Perfect":
            if repeat:
                from PerfectStrategy import simulations as perfect
                results = perfect(numberofsims)
            else:
                from PerfectStrategy import game
                results = game(numberofsims)
        elif strategy == "Monte Carlo":
            if repeat:
                pass
            else:
                from montecarlo import game as game
                # results, HRM = monte(numberofsims)
                results, HRM = game(numberofsims)
                # print(HRM)
                self.controller.shared_data["HRM"] = HRM


        self.controller.shared_data["results"] = results
        self.popup(results)
        self.controller.show_frame("Results")

    def popup(self, results):
        top = tk.Toplevel()
        top.geometry("600x600")
        top.title("Simulation Finished")
        maintext = tk.Label(top, text="The simulation finished! Hurrah", font=TITLE_FONT)
        maintext.pack()
        timetext = "The simulation took " + str(results["Time"])
        timetaken = tk.Label(top, text=timetext, font=LARGE_FONT)
        timetaken.pack()
        close = tk.Button(top,text="See more results", command=top.destroy)
        close.pack()

    def Toggle(self):
        if self.strategy.get() == "Simple":
            self.basicbutton.config(state=tk.NORMAL)
            self.basicbutton.insert(0, "")
            self.basicbutton.pack()
            self.hittolabel.lift()
        else:
            self.hittolabel.lower()
            self.basicbutton.config(state=tk.DISABLED)
            self.basicbutton.pack()

    def initUI(self):
        self.hittolabel.lower()

class Main_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Main Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        button1 = tk.Button(self, text="Go to the input page",
                           command=lambda: controller.show_frame("Input_Page"))
        button1.pack()



class About_Page(tk.Frame):

    def initUI(self):
        pass
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="About Page", font=TITLE_FONT)
        label.pack(pady=10, padx=10)

        maintext = tk.Label(self, text="""This program serves to simulate casino blackjack played with one player and one dealer. This simulation allows for a variety of strategies to provide useful results. This includes:
	• Simple Strategy (The player simply hits until a given amount),
	• Basic Strategy (The player carefully follows a generic preprepared ruleset for every scenario),
	• Perfect Strategy(The player follows the Basic Strategy ruleset but with the accompaniment of perfect card counting and variable wagering to take advantage of this fact)
	• Machine Learning(The program plays randomly in each scenario at first but records its results and begins to adapt what it is the best play for each scenario).

It allows for a variety of simulation arguments and when the simulation is finished, the results are shown as raw data and as well as informative graphs.
This program can take advantage of multiple computers for the simulation if able and configured correctly.""")
        maintext.pack()

        button1 = tk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame("StartPage"))
        button1.pack()

class Results(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the results Page", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        self.results = self.controller.shared_data["results"]
        self.create_table()
        # Show results
        # refresh_grid = tk.Button(self, text="Refresh the grid", command=self.refresh_results)
        # refresh_grid.pack()

        self.saving = tk.BooleanVar()
        tosaveornottosave = tk.Checkbutton(self, text="Save results to file", variable=self.saving, command=self.toggle)
        tosaveornottosave.pack()

        self.confirm = tk.Button(self, text="Are you sure?", command=self.saveresults, state=tk.DISABLED)
        self.confirm.pack()

        graphs = tk.Button(self, text="Go to the graphs page", command=lambda: controller.show_frame("GraphPage"))
        graphs.pack()

    def initUI(self):
        self.refresh_results()
    def create_table(self):
        Labels = ["Total Games", "Total Player wins", "Total dealer wins", "Percentage netgain",
                  "Percentage winrate", "Time Taken"]
        numbers = [0, 0, 0, 0, 0, 0]  # np.zeros(5)

        subframe = tk.Frame(self, width=200, height=200)
        subframe.pack()
        self.label_grid = [[] for i in range(len(Labels))]
        for i in range(len(Labels)):
            self.label_grid[0].append(tk.Label(subframe, text=Labels[i], font=NORM_FONT))
            self.label_grid[1].append(tk.Label(subframe, text=numbers[i], font=NORM_FONT))
            self.label_grid[0][i].grid(column=0, row=i)
            self.label_grid[1][i].grid(column=1, row=i)

    def refresh_results(self):
        dictionary = self.controller.shared_data["results"]

        self.label_grid[1][0].config(text=str(dictionary["Total Games"]))
        self.label_grid[1][2]["text"] = dictionary["Total dealer wins"],
        self.label_grid[1][1]["text"] = dictionary["Total player wins"]
        self.label_grid[1][3]["text"] = round(dictionary["Percentage netgain"], 3)
        self.label_grid[1][4]["text"] = round(dictionary["Percentage winrate"], 4)
        self.label_grid[1][5]["text"] = round(dictionary["Time"], 4)

    def toggle(self):
        var = self.saving.get()
        if var:
            self.confirm.config(state=tk.NORMAL)
        else:
            self.confirm.config(state=tk.DISABLED)



    def saveresults(self):

        dictionary = self.controller.shared_data["results"]

        formatted_time = datetime.datetime.now().strftime("%Y-%m-%d; %H-%M-%S")
        os.mkdir(formatted_time)
        np.save(os.path.join(formatted_time, "dictionary.npy"), dictionary)


class GraphPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.strategy = self.controller.shared_data["strategy"]
        self.repeat = self.controller.shared_data["repeat"]

        label = tk.Label(self, text="This is the graph page", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        # button = tk.Button(self, text="Go to the start page",
        #                    command=lambda: controller.show_frame("StartPage"))
        # button.pack()
        # if self.repeat == True:
        #     GraphTypes = ['Normal Distribution', 'Net gain over time', 'Histogram']
        # else:
        #     GraphTypes = ['Net gain over time', 'Histogram']
        self.GraphTypes = ['Normal Distribution', 'Net gain over time', 'Histogram']
        self.graph = tk.StringVar()
        self.graph.set(self.GraphTypes[0])

        self.dropdown = tk.OptionMenu(self, self.graph, *self.GraphTypes)
        self.dropdown.pack()

        if self.strategy.get() == "Monte Carlo":

            self.HRMVar = tk.BooleanVar()
            self.HRMVar.set(False)
            HRMtoggle = tk.Checkbutton(self, text="Show the AI Strategy colourmap", variable=self.HRMVar)
            HRMtoggle.pack()

        startbtn = tk.Button(self, text="Plot the graphs", command=self.start)
        startbtn.pack()

    def initUI(self):
        self.repeat = self.controller.shared_data["repeat"].get()
        self.strategy = self.controller.shared_data["strategy"].get()
        if self.repeat:
            print("Did repeat")
            self.GraphTypes = ['Normal Distribution', 'Net gain over time', 'Histogram']
        else:
            print("Did not repeat")
            self.dropdown['menu'].delete(0)
            self.graph.set(self.GraphTypes[1])
        if self.strategy == "Monte Carlo":
            self.HRMVar = tk.BooleanVar()
            self.HRMVar.set(False)
            HRMtoggle = tk.Checkbutton(self, text="Show the AI Strategy colourmap", variable=self.HRMVar)
            HRMtoggle.pack()



    def start(self):
        # top = tk.Toplevel()
        # top.geometry("600x600")
        # top.title("Graph Results")
        # text = str(self.graph.get()) + " for "+ str(self.strategy.get())
        # maintext = tk.Label(top, text=text, font=TITLE_FONT)
        # maintext.pack()
        self.equation(self.graph.get())
        # f = Figure(figsize=(5,4), dpi=100)
        # a = f.add_subplot(111)
        # close = tk.Button(top, text="See more results", command=top.destroy)
        # close.pack()

    def equation(self, graphtype):
        dictionary = self.controller.shared_data["results"]
        if graphtype == "Histogram":
            print(dictionary["Strategy"])
            labels, values = zip(*Counter(dictionary["Strategy"]).items())

            indexes = np.arange(len(labels))
            width = 1

            plt.bar(indexes, values, width)
            text = str(self.graph.get()) + " for " + str(self.strategy)
            plt.title(text)
            plt.xticks(indexes + width * 0.5, labels)
            plt.ylabel("Frequency")
            plt.show()
        if graphtype == 'Normal Distribution':
            #print(dictionary["Gainz"])
            plt.figure()
            data = dictionary["Gainz"]
            mean = np.mean(data)
            variance = np.var(data)
            pdf_x = np.linspace(np.min(data), np.max(data), 100)
            pdf_y = 1.0/np.sqrt(2*np.pi*variance)*np.exp(-0.5*(pdf_x-mean)**2/variance)
            plt.hist(dictionary["Gainz"], 100, normed=True,label="Data")
            plt.plot(pdf_x, pdf_y, 'k--', label="Fit")
            plt.legend()
            text = "Normal Distribution for " + str(self.strategy)
            plt.title(text + " " + r'$ \mu=%.3f,\ \sigma=%.3f$' %(mean, np.sqrt(variance)))
            plt.xlabel("Percentage Netgain")
            plt.ylabel("Frequency")
            plt.show()
        if graphtype == "Net gain over time":
            games = dictionary["Total Games"]
            x = np.linspace(0, games, games/50)

            y = dictionary["Netgain over time"]
            plt.plot(x, y)
            text = str(self.graph.get()) + " for " + str(self.strategy)
            plt.xlabel("Simulation number")
            plt.ylabel("Percentage Netgain")
            plt.title(text)
            plt.show()


if __name__ == "__main__":
    app = SampleApp()
    app.geometry("1280x720")
    app.mainloop()
