
class HCLGenerationConfig():
    hcl_block_start = "{"
    hcl_block_end = "}"
    
    ##
    # The character to use for indentations. (Default: SPACE)
    hcl_indentation_character = " "

    ##
    # The number of times to pre-pend the indentation charachter to each indented block. (Default: 2)
    hcl_indentation_count = 2

    hcl_element_seperator = ", "

    hcl_newline = "\n"

    def __init__(self) -> None:
        pass

class HCLConfig:
    ##
    # Configuration to use for Generation
    hcl_generation_config = HCLGenerationConfig()
    
    def __init__(self) -> None:
        pass

class HCLGen():
    indent = HCLGenerationConfig.hcl_indentation_character * HCLGenerationConfig.hcl_indentation_count
    line = HCLGenerationConfig.hcl_newline
    block_start = HCLGenerationConfig.hcl_block_start
    block_end = HCLGenerationConfig.hcl_block_end
    sep = HCLGenerationConfig.hcl_element_seperator
