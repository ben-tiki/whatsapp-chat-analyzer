import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

class VisualConfig:

    # green color palette using seaborn
    palette = sns.color_palette('Greens', 10)
    # set the color palette of the plots
    sns.set_palette(palette)
    # add every font at the specified location
    font_dir = ['fonts']
    for font in font_manager.findSystemFonts(font_dir):
        font_manager.fontManager.addfont(font)

    # set the font to Montserrat
    custom_font = font_manager.FontProperties(fname='fonts\Lato-Regular.ttf')
    # set the font of the plots
    plt.rcParams['font.family'] = custom_font.get_name()
    # set the style of the plots
    sns.set_style('whitegrid', {'font.family': custom_font.get_name(), 'font.serif': custom_font.get_name()})
    # set the context of the plots (Jupyter notebook)    
    sns.set_context('notebook', font_scale=1.5, rc={'lines.linewidth': 2.5})
    # set the size of the plots
    plt.rcParams['figure.figsize'] = (8, 8)
    # set the background color of the plots
    sns.set_color_codes('pastel')
    # make legends transparent
    plt.rcParams['legend.framealpha'] = 1
