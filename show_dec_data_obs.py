from enc_obs import *


__version__ = '1.0.0'


def show_decryption_data(master_password, category):
    system_action('clear')
    separator = ''
    if category == 'note':
        # Костыль
        separator += '    '
    print(PURPLE, "     ___________________________________")
    print(PURPLE, "    /\/| ", YELLOW, "\/                   \/", PURPLE, " |\/\ ")
    print(PURPLE, "   /\/\|", YELLOW, " \/  Saved " + category + 's' + separator + "  \/ ", PURPLE, "|/\/\ ", DEFAULT_COLOR)
    print(YELLOW, "           \/                   \/ ", DEFAULT_COLOR)
    print('\n'*5)

    s = 0

    type_folder = ''
    if category == 'resource':
        type_folder = FOLDER_WITH_RESOURCES
    elif category == 'note':
        type_folder = FOLDER_WITH_NOTES

    for category_item in os.listdir(type_folder):
        decryption_data = dec_only_base64(category_item, master_password)
        s += 1
        print(PURPLE, str(s) + '.', YELLOW, decryption_data, DEFAULT_COLOR)
    if category == 'resource':
        backup_message = ''
        if os.path.exists(OLD_ELBA):
            backup_message = '\n  - Enter "-o" to rollback'
        print(BLUE +
              '\n  - Enter "-r" to restart, "-x" to exit'
              '\n  - Enter "-a" to add new resource'
              '\n  - Enter "-c" to change master-password'
              '\n  - Enter "-d" to remove resource'
              '\n  - Enter "-n" to go to notes'
              '\n  - Enter "-u" to update program'
              '\n  - Enter "-z" to remove ALL data', backup_message,
              YELLOW,
              '\n Select resource by number \n', DEFAULT_COLOR)
    if category == 'note':
        print(BLUE + '\n  - Press "Enter" to go back'
                     '\n  - Enter "-a" to add new note'
                     '\n  - Enter "-x" to exit'
                     '\n  - Enter "-d" to remove note',
              YELLOW, '\n Select note by number \n', DEFAULT_COLOR)
    if s == 0:
        print(YELLOW + '\n    No' + ' saved ' + category + 's \n')
