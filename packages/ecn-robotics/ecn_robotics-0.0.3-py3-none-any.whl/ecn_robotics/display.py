import numpy as np
from colorama import Fore, Back, Style

__n_print = 1
prefixes = [
    [0, 1e-6, Fore.RED],  # If <= 1E-6
    [1e6, float("inf"), Fore.YELLOW],  # If >= 1E6
    [0., 0., Fore.LIGHTBLACK_EX + Style.DIM]  # If == 0
]

input_prefix = f"{Fore.CYAN}"
reset_all = Fore.RESET+Style.RESET_ALL+Back.RESET


def print_input(txt: str) -> int:
    """
    Print a formatted input to the screen.\n
    CÔTE Geoffrey - 2023
    :param txt: the input text hinting
    :return: the inputted number
    """
    return int(input(f"{input_prefix}{txt} {Fore.RED}>{reset_all} "))


def print_choices(choices: dict) -> int:
    """
    Print a choice and return which item was picked.\n
    CÔTE Geoffrey - 2023
    :param choices: a dict with the shape {return_value: text, ...}
    :return: the choice made
    """
    print(f"{input_prefix}Select your mode :{reset_all}")

    # Create mapping
    mapping = {}
    i = 1
    for k, v in choices.items():
        mapping[i] = k
        print(f"\t{Fore.YELLOW}{i}{Fore.RESET} → {Style.BRIGHT+Fore.LIGHTBLACK_EX}{v}{Style.RESET_ALL+Fore.RESET}")
        i += 1

    # Mode selection
    user_choice = -1
    while user_choice <= 0 or user_choice > i:
        user_choice = print_input("Mode")
    return mapping[user_choice]


def print_header(txt: str or list, width: int = 120) -> None:
    """
    Print a header with the given text.\n
    CÔTE Geoffrey - 2023
    :param txt: the text to print
    :param width: the width of the header
    """
    print("╔"+"".center(width-2, "═")+"╗")
    if type(txt) is list:
        for i in range(len(txt)):
            print("║"+Fore.YELLOW+Style.BRIGHT+txt[i].center(width-2, " ")+Fore.RESET+Style.RESET_ALL+"║")
    else:
        print("║" + Fore.YELLOW + Style.BRIGHT + txt.center(width - 2, " ") + Fore.RESET + Style.RESET_ALL + "║")
    print("╚" + "".center(width - 2, "═") + "╝")


def print_matrix(matrix: np.ndarray, xaxis: list = None, yaxis: list = None, name: str = "", width: int = 11) -> None:
    """
    Print a formatted view of the given matrix.\n
    CÔTE Geoffrey - 2023
    :param np.ndarray matrix: the matrix to show
    :param list xaxis: the name of each column
    :param list yaxis: the name of each line
    :param str name: the name of the matrix
    :param int width: the width of a single cell
    """
    global __n_print
    if name == "":
        name = f"Table {__n_print}"
        __n_print += 1

    n = np.shape(matrix)
    if len(n) == 1:
        n = [1, n[0]]

    ###################################################
    #                       Header
    ###################################################
    line_prefix = Fore.LIGHTBLACK_EX
    # Print pre header line
    print(line_prefix+"".center(width, "━"), end="┳")
    print("".center((width + 1) * n[1], "━"), end="")
    print()

    # Print header line
    print(f"{Fore.GREEN}{name[0:width].center(width, ' ')}{Fore.RESET}", end=f"{line_prefix}┃{Style.BRIGHT + Fore.LIGHTCYAN_EX}")
    if xaxis is not None:
        for i in range(n[1]):
            if i < len(xaxis):
                print((" " + xaxis[i])[0:width].center(width, " "), end=" ")
            else:
                print("".center(width, " "), end=" ")
    print(Fore.RESET + Style.RESET_ALL)

    # Print post header line
    print(line_prefix+"".center(width, "━"), end="╋")
    print("".center((width + 1) * n[1], "━"), end=f"{reset_all}")
    print()

    val = lambda r, c: matrix[c] if n[0] == 1 else matrix[r, c]

    ###################################################
    #                       TABLE
    ###################################################
    for row in range(n[0]):

        #                   Y Axis
        if yaxis is not None and len(yaxis) > row:
            print(yaxis[row][0:width].center(width, " "), end=f"{line_prefix}┃{reset_all}")
        else:
            print("".center(width, " "), end=f"{line_prefix}┃{reset_all}")

        #                   Table values
        for col in range(n[1]):
            # Select the right prefix to use for this number
            prefix = Fore.RESET+Style.RESET_ALL+Back.RESET
            for low, high, p in prefixes:
                if low <= np.fabs(val(row, col)) <= high:
                    prefix = prefix+p

            # Format the number format
            num = f"{val(row, col):.5}"
            if num[0] != "-":
                num = " " + num
            num = num.center(width, " ")

            # Show it
            print(f"{prefix}{num}{Fore.RESET + Style.RESET_ALL}", end=" ")
        print()
