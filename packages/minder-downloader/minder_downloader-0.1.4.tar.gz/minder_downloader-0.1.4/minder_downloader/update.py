

import getpass
import webbrowser



def get_token() -> str:
    """get_token opens the access-tokens website to create a unique REST token 

    Returns:
        str: a token generated at https://research.minder.care/portal/access-tokens
    """
    webbrowser.open('https://research.minder.care/portal/access-tokens')
    print('Please copy your token')
    token = getpass.getpass(prompt='Token: ')
    return token