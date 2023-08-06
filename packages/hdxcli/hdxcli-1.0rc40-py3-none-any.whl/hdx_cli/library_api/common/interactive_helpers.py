from typing import Any, Iterable, List, Optional, Tuple, Sequence


__all__ = ['choose_interactively',
           'choose_from_elements_interactively']


def choose_interactively(prompt, *,
                         default: Optional[str] = None,
                         valid_choices: Optional[List[str]] = None) -> str:
    choice = None
    while not choice or choice not in valid_choices:
        choice = input(prompt)
        if choice == '' and default:
            return default
        if not valid_choices:
            return choice
        if choice in valid_choices:
            return choice
        print(f'Invalid choice {choice}. Valid values are {valid_choices}')


def choose_from_elements_interactively(elements: Sequence[Any]) -> Tuple[int, str]:
    """Choose an index from a list of choices and return the index based on 0-offset.
    and the field name
    """
    for i, a_field in enumerate(elements, 1):
        print(f'{i}. {a_field}')
    print()
    element_index = int(choose_interactively(
        'Please choose an index from the list: ',
        valid_choices=[str(x + 1) for x in range(len(elements))]))
    return element_index - 1, elements[element_index - 1]
