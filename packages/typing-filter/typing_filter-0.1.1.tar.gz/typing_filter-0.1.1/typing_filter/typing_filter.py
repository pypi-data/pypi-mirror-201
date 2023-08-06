#!/usr/bin/env python3
"""Uses live user input to filter out potential results.

**Author: Jonathan Delgado**

"""
#------------- Imports -------------#
import sys
import curses
import enum
#--- Custom imports ---#
#------------- Fields -------------#
class Keys(enum.IntEnum):
    """ Keys used for escaping curses. """
    ENTER = 10
    ESCAPE = 27
    SPACE = 32
    BACKSPACE = 127

#======================== Helper ========================#
def is_text_key(key):
    """ Returns True if the key is alphabetic or a space. """
    return 65 <= key <= 122 or key == Keys.SPACE


def filter_options_and_descriptions(filter_string, options, descriptions):
    """ Filter the options shown based off of the user's input.
        
        Args:
            filter_string (str): the user input string to filter by.

            options (list): the list of possible options to filter.
    
        Returns:
            (list): the filtered options.
    
    """
    filtered_options = []
    filtered_descriptions = []
    # Case insensitive
    filter_string = filter_string.lower().strip()
    for index, option in enumerate(options):
        if filter_string in option.lower():
            filtered_options.append(option)
            filtered_descriptions.append(descriptions[index])

    return filtered_options, filtered_descriptions


#======================== Terminal Helper ========================#
def get_terminal_height(stdscr):
    return stdscr.getmaxyx()[0]


def get_list_positions_on_screen(height):
    """ The y position to write the top of the list and the bottom of the list. """
    return 3, height - 5


#======================== Initialization ========================#
def _init_colors():
    """ Initialize colors for use in Curses. """
    curses.start_color()
    # Normal
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    # Incorrect
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    # Notice
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)


def _init_screen(stdscr):
    # Clear and refresh the screen for a blank canvas
    stdscr.erase()
    stdscr.refresh()
    _init_colors()


#======================== Main ========================#
def _filter_selector(stdscr,
        header, prompt,
        selector, selector_padding,
        options, descriptions, description_separator
    ):
    """ Main filter loop.
        
        Args:
            stdscr (): the screen to write the options to.

            header (str): the header to print at the top when providing options.

            prompt (str): the text for the input prompt.

            selector (str): the selector icon, to indicate the highlighted choice, i.e. an arrow.

            selector_padding (int): the amount of spacing to put between the arrow and the options text.

            options (list): the list of options to choose/filter from.

            description_separator (str): the string to separate the option from its description.
    
        Returns:
            (str/None): the selected choice. None if none was chosen.
    """
    #------------- Helper functions -------------#
    def scrollable():
        """ Is the list long enough to support scrolling. """
        return num_options > list_height

    def at_top(): return start == 0 and select_y == list_top

    def at_bottom(): return end == num_options and select_y == last_opt_y

    def options_fit():
        """ Whether all of the options fit in the terminal window. """
        return num_options < list_height

    def get_last_opt_y():
        """ Gets the y position of the last option of the list. """
        # If the list is shorter than the cap, give the current list length
            # zero-indexed.
        rel_y = num_options if options_fit() else list_height
        # Offset the relative y from the start of the list.
        return rel_y + list_top - 1

    def scroll_up():
        nonlocal start, end, select_y
        select_y = list_top

        if not scrollable() or at_top(): return
        start -= 1; end -= 1

    def scroll_down():
        """ Handles scrolling down the filtered list. """
        nonlocal start, end, select_y
        select_y = last_opt_y
        if not scrollable() or at_bottom(): return
        start += 1; end += 1

    def get_select_index():
        """ Get the index of the selected choice based off of the selector's position. """
        return select_y - list_top + start

    def render_scroll_arrows():
        """ Renders scrolling arrows if applicable. """
        if not scrollable(): return
        # Don't draw arrows if there's no reason to or there's no
        # space for them
        if start > 0 and list_top > 0:
            stdscr.addstr(list_top - 1, padding, '↑↑↑')

        if end < num_options:
            stdscr.addstr(list_bottom + 1, padding, '↓↓↓')

    def render_selector():
        # Draw the selector
        # Rewrite the selected line for emphasis
        nonlocal selected_choice
        if num_options > 0:
            # The highlighted choice is valid
            stdscr.attron(curses.color_pair(1))
            selected_choice = filtered_options[get_select_index()]
            stdscr.addstr(select_y, 0, selector)
            stdscr.addstr(select_y, padding, selected_choice)
            stdscr.attroff(curses.color_pair(1))
        else:
            # Draw a red selector for no choices
            stdscr.attron(curses.color_pair(2))
            selected_choice = None
            stdscr.addstr(select_y, 0, selector)
            stdscr.addstr(select_y, padding, 'None')
            stdscr.attroff(curses.color_pair(2))


    def update_input_field(text):
        """ Updates the user input field. Used to write the typed contents thus far. """
        stdscr.addstr(prompt_y + 1, 0, text)

    def update_header():
        stdscr.addstr(0, 0, header, curses.color_pair(3))

    #------------- Initialization -------------#
    _init_screen(stdscr)
    # Vertical padding between channel names and arrow
    padding = selector_padding + len(selector)

    # Initialize descriptions
    if descriptions is None: descriptions = [None] * len(options)

    # Terminal dimensions
    height = get_terminal_height(stdscr)
    # The y placements of the list on the screen
    list_top, list_bottom = get_list_positions_on_screen(height)
    list_height = list_bottom - list_top + 1
    # y position for user input prompt
    prompt_y = height - 2

    #--- Declarations ---#
    # The typed string thus far
    user_string = ''
    # y position of selector, start at the top
    select_y = list_top
    num_options = len(options)
    # The y position of the last option
    last_opt_y = get_last_opt_y()
    # Start and end of sublists for scrolling of longer lists
    start, end = 0, list_height
    # Truncate the view in the case where the list is too long
    selected_choice = options[0]
    key = 0
    filtered_options = options[:]
    filtered_descriptions = descriptions[:]
    #------------- Body -------------#
    while key not in [Keys.ENTER, Keys.ESCAPE]:
        # Clear the screen for the next update in this loop
        stdscr.erase()
        # Flag for indicating the user_string was changed
        user_typed = False

        #------------- Key parsing -------------#
        if is_text_key(key):
            # Create the user string as it's typed
            user_string += chr(key)
            user_typed = True
        elif key == Keys.BACKSPACE and len(user_string) > 0:
            # Backspace was pressed, delete it
            user_string = user_string[:-1]
            user_typed = True
        elif key == curses.KEY_DOWN: select_y += 1
        elif key == curses.KEY_UP: select_y -= 1

        #--- Filter options ---#
        if user_typed:
            filtered_options, filtered_descriptions = filter_options_and_descriptions(user_string, options, descriptions)
            num_options = len(filtered_options)
            # Get the new y position of the last option in case the list
                # was shortened
            last_opt_y = get_last_opt_y()

            # Reset the sublist view
            start, end = 0, list_height

        #------------- Cursor wrapping -------------#
        if num_options == 0: select_y = list_top
        elif select_y > last_opt_y:
            # We're below the last list option on screen
            if key == curses.KEY_DOWN: scroll_down()
            else:
                # The filtered_options list is just shorter than before
                select_y = last_opt_y
        elif select_y < list_top and key == curses.KEY_UP: scroll_up()

        #------------- Rendering -------------#
        for row, option in enumerate(filtered_options[start:end]):
            desc = filtered_descriptions[start:end][row]
            item = option if desc is None else option + description_separator + desc
            try:
                stdscr.addstr(list_top + row, padding, item)
            except:
                print('Failed to write list choices to terminal. Terminal window may be too small to continue.')
                sys.exit()


        render_scroll_arrows()
        render_selector()
        update_header()
        update_input_field(f'{prompt} {user_string}')

        # Refresh the screen
        stdscr.refresh()
        # Wait for next input, get as number for easier checking
        key = stdscr.getch()


    if key == Keys.ENTER: return selected_choice
    if key == Keys.ESCAPE: return None


def launch(
        options,
        descriptions=None,
        description_separator=' - ',
        header='Press Escape or Ctrl + C to quit...',
        prompt='Search options:',
        selector='-->', selector_padding=2
    ):
    return curses.wrapper(_filter_selector, **locals())


#======================== Entry ========================#

def main():
    import rich.traceback; rich.traceback.install()
    # Testing
    options = ['Alabama', 'Alaska', 'American Samoa', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Guam', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Minor Outlying Islands', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Northern Mariana Islands', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'U.S. Virgin Islands', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
    descriptions = [None] * len(options)
    descriptions[3] = 'This is a state.'
    
    selected = launch(options=options, descriptions=descriptions)
    print( f'Selected: {selected}', )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()