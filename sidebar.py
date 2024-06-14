from streamlit import sidebar, image, info, __version__
from streamlit_option_menu import option_menu

def app_sidebar():
    with sidebar:
        mode = option_menu(
            'Audio DataProc',
            ['Annotation', 'Record', 'Tutorial'],
            icons=['chat-left-text', 'record-btn', 'book-half'],
            menu_icon='emoji-wink',
            default_index=0
        )
        image('assets/soundwave.png')
        info(f"Streamlit Version:{__version__}")

    return mode  