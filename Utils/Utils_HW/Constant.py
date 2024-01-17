class Constant(object):
    """In this class, we use HTML attributes as constants
    Args:
        object: HTML attribute
    Raises:
        Exception: return the exception whenever someone tries to\
            assign a new value to the class attribute
    """
    
    CLASS_EDU_EXP = {'class' : 'tw-flex tw-flex-wrap tw-gap-3 lg:tw-mb-3'}
    CLASS_SAL_COM = {'class' : 'tw-mb-3 tw-flex'}
    CLASS_CON_LOC = {'class' : 'tw-tag-contract-s tw-readonly'}
    CLASS_REM_DUR = {'class' : 'tw-flex tw-gap-3 tw-flex-wrap tw-mb-3 tw-whitespace-nowrap'}
    CLASS_SAL_EST = {'class': 'tw-flex tw-flex-col sm:tw-flex-row tw-mb-8 sm:tw-items-center'}
    CLASS_DESC = {'class': 'tw-typo-long-m tw-mb-12 sm:tw-mb-14 tw-break-words'}
    
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
                (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    def __setattr__(self, *_):
        raise Exception("Tried to change the value of a constant")