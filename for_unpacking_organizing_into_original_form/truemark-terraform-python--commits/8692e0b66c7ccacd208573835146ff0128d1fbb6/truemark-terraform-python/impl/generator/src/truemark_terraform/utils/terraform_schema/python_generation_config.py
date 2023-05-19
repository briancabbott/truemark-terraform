
##
# General, all settings container. 
class PyGenerationConfig():

    ##
    # The character to use for indentations. (Default: SPACE)
    py_indentation_character = " "

    ##
    # The number of times to pre-pend the indentation charachter to each indented block. (Default: 2)
    py_indentation_count = 4

    py_element_seperator = ", "

    py_newline = "\n"

    def __init__(self) -> None:
        pass

##
# Intermediate 
class PyConfig:
    ##
    # Configuration to use for Generation
    py_generation_config = PyGenerationConfig()
    
    def __init__(self) -> None:
        pass


class PyGen:
    indent = PyConfig.py_generation_config.py_indentation_character * PyConfig.py_generation_config.py_indentation_count
    line = PyConfig.py_generation_config.py_newline
    # # block_start = PyConfig.py_generation_config.py_block_start
    # block_end = PyConfig.py_generation_config.
    # sep = PyConfig.
