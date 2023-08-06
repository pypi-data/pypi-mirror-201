import os

from colorama import Back, Fore, Style


class Colored:

    _RESET = Style.RESET_ALL

    @classmethod
    def get_color_prefix(cls, color=None, color_prefix=None, prefix_msg=None,
                         bottom=False, bottom_color=None, bottom_prefix=None,
                         bottom_msg=None):
        """
        show prefix in terminal as below:

           zone1 zone2
           |    | |
            mkie

                   zone3
                  |     |
            mkie xxx 
        """
        # zone1
        color = color or 'BLACK'
        color_prefix = Style.BRIGHT + color_prefix + getattr(Back, color)
        prefix_msg = prefix_msg or os.path.basename(os.getcwd())
        color_edge = getattr(Fore, color, None)

        zone1 = f'\n{color_edge}{color_prefix}{prefix_msg}{cls._RESET}'

        if not bottom:
            zone2 = f'{color_edge}'
            return f'{zone1}{zone2}{cls._RESET} '

        # bottom
        bottom_color = bottom_color or 'BLACK'
        bottom_prefix = bottom_prefix + getattr(Back, bottom_color)
        bottom_edge = getattr(Fore, bottom_color, None)

        color_edge += getattr(Back, bottom_color)

        zone2 = f'{color_edge} '
        zone3 = f' {bottom_prefix}{bottom_msg} {cls._RESET}{bottom_edge}'

        return (f'{zone1}{zone2}{zone3}{cls._RESET}')

    @classmethod
    def draw(cls, color=None, msg=None):
        """
        colored msg only
        """
        return f'{color}{msg}{cls._RESET}'
