'''
Main module with all of the functions

* in principle, we require no extra module
* all modules are loaded within the functions
'''


import os

def set_fig_rule(f=None, g=True, delete=True):
    """
    Function to set rules for matplotlib figures.

    It is very useful when trying to figure out margins and locations of access.

    Parameters
    ----------
    f : matplotlib.figure.Figure, optional
        The figure object to be modified. If not given, the current figure will be used. Default is None.
    g : bool, optional
        A flag to turn on/off grid lines. Default is True.
    delete : If true, then, the file is deleted automatically. Otherwise you are supposed to do it

    Returns
    -------
    The path to the temporary file

    Examples
    ------
        Create a sample figure

        >>> fig, ax = plt.subplots()
        >>> ax.plot([1, 2, 3], [4, 5, 6])

        Apply the figure rules using the set_fig_rule function

        >>> set_fig_rule(f=fig, g=True)

    """

    import matplotlib as plt


    # If no figure is provided, get the current one
    if f is None:
        f: plt.Figure = plt.gcf()

    # Set the figure background color and add axes
    f.patch.set_color('.9')
    ax = f.add_axes([0, 0, 1, 1])
    ax.patch.set_alpha(0)
    ax1: plt.Axes = f.add_axes([0, 0, 1, 1])
    ax1.patch.set_alpha(0)

    # Set limits and tick positions
    x, y = f.get_size_inches()
    ax1.set_xlim(0, x)
    ax1.set_ylim(0, y)
    ax1.xaxis.tick_top()
    ax1.xaxis.set_label_position('top')
    ax1.yaxis.tick_right()
    ax1.yaxis.set_label_position('right')

    # Set labels for axes
    ax.set_ylabel('fig')
    ax1.set_ylabel('inch')
    ax.set_xlabel('fig')
    ax1.set_xlabel('inch')

    # Set colors for lines and labels
    cf_ = 'C4'
    cI_ = 'C5'
    ax.spines['bottom'].set_color(cf_)
    ax.xaxis.label.set_color(cf_)
    ax.tick_params(axis='x', colors=cf_)
    ax.spines['left'].set_color(cf_)
    ax.yaxis.label.set_color(cf_)
    ax.tick_params(axis='y', colors=cf_)

    # Turn on/off grid lines
    if g:
        ax.grid(c=cf_, alpha=.1, lw=2, ls=':')
        ax1.grid(c=cI_, alpha=.1, lw=2, ls='-.')

    # Save and display the figure
    # pdf = '/tmp/rf.pdf'
    pdf = save_fig_temp_sys_open(f, delete)

    return pdf.name


def save_fig_temp_sys_open(f, delete=True):
    """
    Saves a Matplotlib figure as a temporary PDF file and opens it using the system's default program.

    Parameters
    ----------
    f : matplotlib.figure.Figure
        The figure object to be saved.
    delete : bool
        A flag to determine whether the temporary file should be deleted after opening.

    Returns
    -------
    tempfile.NamedTemporaryFile
        A file object representing the temporary PDF file.

    Notes
    -----
    This function is particularly useful when creating figures for scientific articles and presentations,
    as it allows you to quickly save and view the figure without having to manually open the file.

    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3], [4, 5, 6])
    >>> save_fig_temp_sys_open(fig, delete=False)
    """
    import tempfile
    pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=delete)
    f.savefig(pdf.name, bbox_inches='tight', transparent=True)

    # Try to open the PDF file using the system's default program
    try:
        # In case the system is Windows
        os.startfile(pdf.name)
    except:
        try:
            # In case the system is Mac
            os.system(f'open {pdf.name}')
        except:
            try:
                # In case the system is Linux
                os.system(f'xdg-open {pdf.name}')
            except:
                pass

    # Pause for a short time to allow the system to open the file before deleting it
    import time
    time.sleep(.005)

    return pdf


def set_margin(f=None, x1=None, x2=None, y1=None, y2=None):
    """
    Adjusts the margins of a matplotlib figure.

    * parameters are absolute in inches—not a proportion of the figure—.

    Parameters
    ----------
    f : matplotlib.figure.Figure, optional
        The figure object to be modified. If not given, the current figure will be used. Default is None.
    x1 : float, optional
        The fraction of the figure width to reserve as padding for the left side of the plot. Default is None.
    x2 : float, optional
        The fraction of the figure width to reserve as padding for the right side of the plot. Default is None.
    y1 : float, optional
        The fraction of the figure height to reserve as padding for the bottom of the plot. Default is None.
    y2 : float, optional
        The fraction of the figure height to reserve as padding for the top of the plot. Default is None.

    Returns
    -------
    None

    Example
    ------
    Create a simple plot and adjust the margins to make room for the legend

    >>> x = [1, 2, 3]
    >>> y = [4, 5, 6]
    >>> fig, ax = plt.subplots()
    >>> ax.plot(x, y)
    >>> set_margin(f=fig, x1=0.1, x2=0.2, y1=0.1, y2=0.2)




    """
    import matplotlib.pyplot as plt
    # If no figure is provided, get the current one
    if f is None:
        f:plt.Figure = plt.gcf()

    # Get the dimensions of the figure
    bbox = f.get_window_extent().transformed(f.dpi_scale_trans.inverted())
    x, y = bbox.width, bbox.height
    # print(x, y)

    # Adjust the margins based on the provided parameters
    if x1 is not None:
        f.subplots_adjust(left=x1/x)
    if x2 is not None:
        f.subplots_adjust(right=1-x2/x)
    if y1 is not None:
        f.subplots_adjust(bottom=y1/y)
    if y2 is not None:
        f.subplots_adjust(top=1-y2/y)