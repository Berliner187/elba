from enc_obs import *


__version__ = '1.1.1'


def show_decryption_data(generic_key, category):
    system_action('clear')
    separator = ''
    if category == 'note':
        separator += '    '
    print(BLUE + "     ___________________________________")
    print(BLUE + "    /\/| ", YELLOW, "\/                   \/", BLUE, " |\/\ ")
    print(BLUE + "   /\/\|", YELLOW, " \/  Saved " + category + 's' + separator + "  \/ ", BLUE, "|/\/\ ", DEFAULT_COLOR)
    print(YELLOW + "           \/                   \/ \n")
    print('\n')

    s = 0

    type_folder = ''
    if category == 'resource':
        type_folder = FOLDER_WITH_RESOURCES
    elif category == 'note':
        type_folder = FOLDER_WITH_NOTES

    for category_item in os.listdir(type_folder):
        decryption_data = dec_only_base64(category_item, generic_key)
        s += 1
        print(BLUE, str(s) + '.', YELLOW, decryption_data, DEFAULT_COLOR)
    if category == 'resource':
        backup_message = ''
        if os.path.exists(OLD_ELBA):
            backup_message = BLUE + '\n  - Enter \'-o\' to rollback               ' + YELLOW + ' |'
        print(
            YELLOW, '\n__________________________________________',
            BLUE, '\n  - Enter \'-r\' to restart, "-x" to exit ', YELLOW, '|',
            BLUE, '\n  - Enter \'-a\' to add new resource      ', YELLOW, '|',
            BLUE, '\n  - Enter \'-c\' to change master-password', YELLOW, '|',
            BLUE, '\n  - Enter \'-d\' to remove resource       ', YELLOW, '|',
            BLUE, '\n  - Enter \'-n\' to go to notes           ', YELLOW, '|',
            BLUE, '\n  - Enter \'-f\' to encrypt your files', RED, 'ALPHA  |',
            BLUE, '\n  - Enter \'-u\' to update program        ', YELLOW, '|',
            BLUE, '\n  - Enter \'-z\' to remove ALL data       ', YELLOW, '|',
            backup_message, YELLOW,
            '\n__________________________________________|\n'
            '\n Select resource by number \n', DEFAULT_COLOR)
    if category == 'note':
        print(
            YELLOW, '\n__________________________________',
            BLUE, '\n  - Press "Enter" to go back    ', YELLOW, '|',
            BLUE, '\n  - Enter "-a" to add new note  ', YELLOW, '|',
            BLUE, '\n  - Enter "-x" to exit          ', YELLOW, '|',
            BLUE, '\n  - Enter "-d" to remove note   ', YELLOW, '|',
            '\n__________________________________|\n',
            YELLOW, '\n Select note by number \n', DEFAULT_COLOR)
    if s == 0:
        print(YELLOW + '\n    No' + ' saved ' + category + 's \n')
