def helper(choice_list):
    print('Choose journal you want to work with: ')
    for item in choice_list:
        print('[{}] {}'.format(item[0], item[2]))


def event(choice_list):
    cmd = 'EMPTY'

    while cmd:
        print('')
        cmd = input('I choose: ')
        cmd = cmd.strip()
        found = True

        for idx, item in enumerate(choice_list):
            if cmd == item[0]:
                print('')
                print('You have chosen: {}'.format(item[2]))
                return idx
            found = False

        if not found:
            print('That\'s not a valid command.')

