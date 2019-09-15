import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.text as mtext


class MyLine(lines.Line2D):
    def __init__(self, *args, **kwargs):
        # we'll update the position when the line data is set
        self.text = mtext.Text(0, 0, '')
        lines.Line2D.__init__(self, *args, **kwargs)

class Show():        
    def show(x, y , distance):
        fig, ax = plt.subplots()
        ax.set_xlim([-10,220])
        ax.set_ylim([-10,220])
        line = MyLine(x, y)
        line.text.set_color('red')
        line.text.set_fontsize(8)
        
        ax.add_line(line)
        ax.text(0,-2,distance)
        plt.show()


