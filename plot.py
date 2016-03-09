import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as tic
from datetime import datetime
from db import BabyDB
#from distutils.version import LooseVersion

xkcd=False
#if LooseVersion(matplotlib.__version__) >= LooseVersion("1.3.1"):
#    xkcd=True
namemap={
        'pipi':'Pipi',
        'kacka': 'Kacka',
        'linkebrust': 'linke Brust',
        'rechtebrust': 'rechte Brust'
        }
linemap={
        'pipi':'#fffc00',
        'kacka': '#4e3700',
        'linkebrust': '#ff0000',
        'rechtebrust': '#00eb1a'
        }
order=['linkebrust','rechtebrust','pipi','kacka']
def plot(x,y,fn="graph.png",start=None):
    actions = y.keys()
    sactions = order[:]
    if set(actions) == set(sactions):
        actions = sactions[:]
    #actions.sort()
    x = [datetime.fromtimestamp(xv) for xv in x]

    if xkcd:
        plt.xkcd()
    fig, ax = plt.subplots()
    cc =ax._get_lines.color_cycle
    for a in actions:
        al=a
        ac=next(cc)
        if namemap.has_key(a):
            al=namemap[a]
        if linemap.has_key(a):
            ac=linemap[a]
        ax.plot_date(x,[ys/3600.0 for ys in y[a]],'-',color=ac,label=al,linewidth=2)
    if start is not None:
        ax.set_xlim([datetime.fromtimestamp(start),datetime.now()])
    window = ax.get_xlim()
    if (window[1]-window[0]) < 5:
        ax.xaxis.set_major_locator(md.HourLocator(byhour=(0,12)))
        ax.xaxis.set_major_formatter(md.DateFormatter('%d.%m.'))
        ax.xaxis.set_minor_locator(md.HourLocator())
        ax.xaxis.set_minor_formatter(md.DateFormatter('%H'))
        if xkcd:
            ax.xaxis.set_tick_params(which="major",pad=25)
        else:
            ax.xaxis.set_tick_params(which="major",pad=15)
        fig.canvas.draw()
        for label in ax.xaxis.get_minorticklabels():
            if label.get_text() not in ('00','06','12','18'):
                label.set_visible(False)
    else:
        ax.xaxis.set_major_locator(md.DayLocator())
        ax.xaxis.set_major_formatter(md.DateFormatter('%d.%m.'))
        #ax.xaxis.set_minor_locator(md.HourLocator())
        #ax.xaxis.set_minor_formatter(md.DateFormatter(''))

    ax.yaxis.set_major_locator(tic.MultipleLocator(12))
    ax.yaxis.set_minor_locator(tic.MultipleLocator(1))
    ax.yaxis.grid(True, which="both",linewidth=1)

    ax.set_title('Baby Tracker')
    ax.set_ylabel('verstrichende Zeit [h]')
    ax.autoscale_view()
    ax.grid(True, linewidth=1)
    if xkcd:
        ax.tick_params(width=2,length=6,which='minor')

    fig.autofmt_xdate(rotation="0", ha="center")
    ax.legend(loc='best')

    fig.savefig(fn,dpi=144)
    #plt.show()

def genplot():
    db=BabyDB()
    x,y = db.preparePlot()
    db.close()
    plot(x,y,"graph_all.png")
    plot(x,y,"graph_24.png",int(time.time()-86400))

if __name__ == "__main__":
    import time
    import os,sys
    np=os.path.dirname(sys.argv[0])
    if np != "":
        os.chdir(os.path.dirname(sys.argv[0]))
    genplot()
