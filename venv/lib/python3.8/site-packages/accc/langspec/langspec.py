# -*- coding: utf-8 -*-
#########################
#       LANGUAGE        #
#########################
"""
This module describes languages specifications for ACCC.
"""


#########################
# IMPORTS               #
#########################
from accc.lexems import *




#########################
# PRE-DECLARATIONS      #
#########################
# keys of 
INDENTATION    = 'indent'
BEG_BLOCK      = 'begin_block'
END_BLOCK      = 'end_block'
BEG_LINE       = 'begin line'
END_LINE       = 'end line'
BEG_ACTION     = 'begin action'
END_ACTION     = 'end action'
BEG_CONDITION  = 'begin condition'
END_CONDITION  = 'end condition'
LOGICAL_AND    = 'logical and'
LOGICAL_OR     = 'logical or'




#########################
# CONSTRUCTION FUNCTION #
#########################
def constructSpec(indentation, begin_block, end_block, begin_line, end_line, 
                  begin_action, end_action, 
                  begin_condition, end_condition, 
                  logical_and, logical_or):
    """Return a language specification based on parameters."""
    return {
        INDENTATION   : indentation, 
        BEG_BLOCK     : begin_block,
        END_BLOCK     : end_block,
        BEG_LINE      : begin_line, 
        END_LINE      : end_line, 
        BEG_ACTION    : begin_action, 
        END_ACTION    : end_action, 
        BEG_CONDITION : begin_condition, 
        END_CONDITION : end_condition, 
        LOGICAL_AND   : logical_and, 
        LOGICAL_OR    : logical_or
    }


#########################
# TRANSLATED FUNCTION   #
#########################
def translated(structure, values, lang_spec):
    """Return code associated to given structure and values, 
    translate with given language specification."""
    # LANGUAGE SPECS
    indentation = '\t'
    endline = '\n'


    object_code = ""
    stack = []
    # define shortcuts to behavior
    push = lambda x: stack.append(x)
    pop  = lambda  : stack.pop()
    last = lambda  : stack[-1] if len(stack) > 0 else ' '
    def indented_code(s, level, end):
        return lang_spec[INDENTATION]*level + s + end

    # recreate python structure, and replace type by value
    level = 0
    CONDITIONS = [LEXEM_TYPE_PREDICAT, LEXEM_TYPE_CONDITION]
    ACTION = LEXEM_TYPE_ACTION
    DOWNLEVEL = LEXEM_TYPE_DOWNLEVEL
    for lexem_type in structure:
        if lexem_type is ACTION:
            # place previous conditions if necessary
            if last() in CONDITIONS:
                # construct conditions lines
                value, values = values[0:len(stack)], values[len(stack):]
                object_code += (indented_code(lang_spec[BEG_CONDITION] 
                    + lang_spec[LOGICAL_AND].join(value) 
                    + lang_spec[END_CONDITION], 
                    level, 
                    lang_spec[END_LINE]
                ))
                # if provided, print the begin block token on a new line
                if len(lang_spec[BEG_BLOCK]) > 0:
                    object_code += indented_code( 
                        lang_spec[BEG_BLOCK],
                        level, 
                        lang_spec[END_LINE]
                    )
                stack = []
                level += 1
            # and place the action
            object_code += indented_code(
                lang_spec[BEG_ACTION] + values[0], 
                level, 
                lang_spec[END_ACTION]+lang_spec[END_LINE]
            )
            values = values[1:]
        elif lexem_type in CONDITIONS:
            push(lexem_type)
        elif lexem_type is DOWNLEVEL:
            if last() not in CONDITIONS:
                # down level, and add a END_BLOCK only if needed
                level -= 1
                if level >= 0:
                    object_code += indented_code(
                        lang_spec[END_BLOCK], level,
                        lang_spec[END_LINE]
                    )
                else:
                    level = 0

    # add END_BLOCK while needed for reach level 0
    while level > 0:
        level -= 1
        if level >= 0:
            object_code += indented_code(
                lang_spec[END_BLOCK], level,
                lang_spec[END_LINE]
            )
        else:
            level = 0
    # Finished !
    return object_code







#########################
# C++                   #
#########################
def cpp_spec():
    """C++ specification, provided for example, and java compatible."""
    return {
        INDENTATION    : '\t',
        BEG_BLOCK      : '{',
        END_BLOCK      : '}',
        BEG_LINE       : '',
        END_LINE       : '\n',
        BEG_ACTION     : '',
        END_ACTION     : ';',
        BEG_CONDITION  : 'if(',
        END_CONDITION  : ')',
        LOGICAL_AND    : ' && ',
        LOGICAL_OR     : ' || '
    }
    




#########################
# ADA                   #
#########################
def ada_spec():
    """Ada specification, provided for example"""
    return {
        INDENTATION    : '\t',
        BEG_BLOCK      : '',
        END_BLOCK      : 'end if;',
        BEG_LINE       : '',
        END_LINE       : '\n',
        BEG_ACTION     : '',
        END_ACTION     : ';',
        BEG_CONDITION  : 'if ',
        END_CONDITION  : ' then',
        LOGICAL_AND    : ' and ',
        LOGICAL_OR     : ' or '
    }
    



#########################
# PYTHON                #
#########################
def python_spec():
    """Python specification, provided for use"""
    return {
        INDENTATION    : '\t',
        BEG_BLOCK      : '',
        END_BLOCK      : '',
        BEG_LINE       : '',
        END_LINE       : '\n',
        BEG_ACTION     : '',
        END_ACTION     : '',
        BEG_CONDITION  : 'if ',
        END_CONDITION  : ':',
        LOGICAL_AND    : ' and ',
        LOGICAL_OR     : ' or '
    }


