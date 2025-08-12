from classes import erase_lines, bc


def get_choice(
        amount_of_choices_to_clear,
        min_choice_possible,
        max_choice_possible
):
    """
    Get the integer permitted choice.

    Parameters
    ----------
    amount_of_choices_to_clear : int
        List of choices to clear.
    min_choice_possible : int
        Minimum possible choice.
    max_choice_possible : int
        Maximum possible choice.

    Returns
    -------
    int
        Choice.
    """
    erased = False
    while True:
        try:
            choice = int(input(f"{bc.UNDERLINE}Your choice:{bc.ENDC} ")) - 1
            if min_choice_possible <= choice <= max_choice_possible:
                if not erased:
                    erase_lines(1)
                else:
                    erase_lines(2)

                erase_lines(amount_of_choices_to_clear)
                return choice

            if not erased:
                erase_lines(1)
                erased = True
            else:
                erase_lines(2)

            print(
                bc.FAIL + bc.UNDERLINE
                + "There is no such a choice!"
                + bc.ENDC
            )
        except ValueError:
            if not erased:
                erase_lines(1)
                erased = True
            else:
                erase_lines(2)

            print(f"{bc.FAIL}{bc.UNDERLINE}Please enter the number!{bc.ENDC}")
