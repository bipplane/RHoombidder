# -*- coding: utf-8 -*-
#########################
# IMPORTS               #
#########################
from math import log, ceil
from itertools import zip_longest
from functools import partial, lru_cache
import itertools

import accc.langspec as langspec 


#########################
# PRE-DECLARATIONS      #
#########################
# lexems seens in structure
from accc.lexems import LEXEM_TYPE_CONDITION, LEXEM_TYPE_ACTION 
from accc.lexems import LEXEM_TYPE_PREDICAT, LEXEM_TYPE_DOWNLEVEL 
# lexems only seen in values
from accc.lexems import LEXEM_TYPE_COMPARISON, LEXEM_TYPE_OPERATOR 
from accc.lexems import LEXEM_TYPE_UINTEGER 
# all lexems
from accc.lexems import ALL as ALL_LEXEMS



#########################
# COMPILER CLASS        #
#########################
class Compiler():
    """
    Compiler of code writed with any vocabulary. ('01', 'ATGC', 'whatevr',…)
    A source code is an ordered list of vocabulary elements 
        ('10011010000101', 'AGGATGATCAGATA', 'wtrvwhttera'…).
    Whatever the given source_code, it's always compilable. (but can return empty object code)
    Also, it can be totally illogic (do many times the same test, do nothing,…)

    The source code is readed entirely for determine STRUCTURE, 
    and then re-readed for determines effectives VALUES.

    The STRUCTURE defines:
        - logic of the code
        - lexems type that will be used
    The VALUES defines:
        - what are the exact value of each lexem
        - values of integers used as function parameters

    Example of prettified STRUCTURE:
     
        if C:
            A
            if C:
                A
                A
                if P and P:
                    A
                    A
                A
            if P:
                A
     
    VALUES will describes which is the lexem effectively used for each
    word, C, A or P. (condition, action, predicat)
    NB: D is the char that indicate a indent level decrease

    The dictionnary values vocabulary, given at compiler creation, define lexems :
     
        vocabulary_values = {
            LEXEM_TYPE_COMPARISON: ('parameter1', 'parameter2', 'parameter3', 'parameter4'),
            LEXEM_TYPE_PREDICAT  : ('have_that', 'is_this', 'have_many_things', 'know_that'),
            LEXEM_TYPE_ACTION    : ('do_that', 'say_this'),
            LEXEM_TYPE_OPERATOR  : ('>', '==', '<', 'is', '!='),
        }
     
    Then, compiled code can be something like:
     
        if parameter1 == parameter2 and have_that:
            do_that
            if have_that:
                say_this
                do_that
                if know_that and have_many_things:
                    do_that
                    say_this
                do_that
            if have_many_things:
                say_this

    Modification of provided lexems types is not supported at this time.
    """
# CONSTRUCTOR #################################################################
    def __init__(self, alphabet, target_language_spec, comparables, predicats, actions, operators, 
                 neutral_value_condition='True', neutral_value_action='pass'):
        """
        Wait for alphabet ('01', 'ATGC',…), language specification and vocabularies of 
            structure and values parts.
        Neutral value is used when no value is finded. 
            Set it to something that pass in all cases.
            NB: a little source code lead to lots of neutral values.
        """
        self.alphabet         = alphabet
        self.voc_structure    = ALL_LEXEMS
        self.target_lang_spec = target_language_spec()
        self.voc_values       = {
            LEXEM_TYPE_COMPARISON: comparables,
            LEXEM_TYPE_PREDICAT  : predicats,
            LEXEM_TYPE_ACTION    : actions,
            LEXEM_TYPE_OPERATOR  : operators,
        }
        self.neutral_value_action    = neutral_value_action
        self.neutral_value_condition = neutral_value_condition
        # verifications
        assert(issubclass(neutral_value_action.__class__, str) 
               and issubclass(neutral_value_condition.__class__, str)
              )
        # prepare tables of words->lexems
        self._initialize_tables()


# PUBLIC METHODS ###############################################################
    def compile(self, source_code, post_treatment=''.join):
        """Compile given source code.
        Return object code, modified by given post treatment.
        """
        # read structure
        structure = self._structure(source_code)
        values    = self._struct_to_values(structure, source_code)
        # create object code, translated in targeted language
        obj_code = langspec.translated(
            structure, values, 
            self.target_lang_spec
        )
        # apply post treatment and return
        return obj_code if post_treatment is None else post_treatment(obj_code)


# PRIVATE METHODS ##############################################################
    def _initialize_tables(self):
        """Create tables for structure and values, word->vocabulary"""
        # structure table
        self.table_struct, self.idnt_struct_size = self._create_struct_table()
        # values table
        self.table_values, self.idnt_values_size = self._create_values_table()
        # debug print
        #print(self.table_struct)
        #print(self.idnt_struct_size)
        #print(self.table_values)
        #print(self.idnt_values_size)

    def _structure(self, source_code):
        """return structure in ACDP format."""
        # define cutter as a per block reader
        def cutter(seq, block_size):
            for index in range(0, len(seq), block_size):
                lexem = seq[index:index+block_size]
                if len(lexem) == block_size:
                    yield self.table_struct[seq[index:index+block_size]]
        return tuple(cutter(source_code, self.idnt_struct_size))

    def _next_lexem(self, lexem_type, source_code, source_code_size):
        """Return next readable lexem of given type in source_code.
        If no value can be found, the neutral_value will be used"""
        # define reader as a lexem extractor
        def reader(seq, block_size):
            identificator = ''
            for char in source_code:
                if len(identificator) == self.idnt_values_size[lexem_type]:
                    yield self.table_values[lexem_type][identificator]
                    identificator = ''
                identificator += char
        lexem_reader = reader(source_code, self.idnt_values_size)
        lexem = None
        time_out = 0
        while lexem == None and time_out < 2*source_code_size: 
            lexem = next(lexem_reader)
            time_out += 1
        # here we have found a lexem
        return lexem
        
    def _next_condition_lexems(self, source_code, source_code_size):
        """Return condition lexem readed in source_code"""
        # find three lexems
        lexems = tuple((
            self._next_lexem(LEXEM_TYPE_COMPARISON, source_code, source_code_size),
            self._next_lexem(LEXEM_TYPE_OPERATOR  , source_code, source_code_size),
            self._next_lexem(LEXEM_TYPE_COMPARISON, source_code, source_code_size)
        ))
        # verify integrity
        if None in lexems: # one of the condition lexem was not found in source code 
            return None
        else: # all lexems are valid
            return ' '.join(lexems)
        

    @lru_cache(maxsize = 100)
    def _string_to_int(self, s):
        """Read an integer in s, in Little Indian. """
        base = len(self.alphabet)
        return sum((self._letter_to_int(l) * base**lsb 
                    for lsb, l in enumerate(s)
                   ))

    @lru_cache(maxsize = None)
    def _letter_to_int(self, l):
        return self.alphabet.index(l)




    @lru_cache(maxsize = 127) # source code is potentially largely variable on length
    def _integer_size_for(self, source_code_size):
        """Find and return the optimal integer size.
        A perfect integer can address all indexes of 
        a string of size source_code_size.
        """
        return ceil(log(source_code_size, len(self.alphabet)))



    def _struct_to_values(self, structure, source_code):
        """Return list of values readed in source_code, 
        according to given structure.
        """
        # iterate on source code until all values are finded
        # if a value is not foundable, 
        #   (ie its identificator is not in source code)
        #   it will be replaced by associated neutral value
        iter_source_code = itertools.cycle(source_code)
        values = []
        for lexem_type in (l for l in structure if l is not 'D'):
            if lexem_type is LEXEM_TYPE_CONDITION:
                new_value = self._next_condition_lexems(
                    iter_source_code, len(source_code)
                )
            else:
                new_value = self._next_lexem(
                    lexem_type, iter_source_code, len(source_code)
                )
            # if values is unvalid:
            #   association with the right neutral value
            if new_value is None:
                if lexem_type in (LEXEM_TYPE_PREDICAT, LEXEM_TYPE_CONDITION):
                    new_value = self.neutral_value_condition
                else:
                    new_value = self.neutral_value_action
            values.append(new_value)

        return values


        



# TABLE METHODS ################################################################
    def _create_struct_table(self):
        """Create table identificator->vocabulary, 
        and return it with size of an identificator"""
        len_alph = len(self.alphabet)
        len_vocb = len(self.voc_structure)
        identificator_size = ceil(log(len_vocb, len_alph))
        # create list of lexems 
        num2alph = lambda x, n: self.alphabet[(x // len_alph**n) % len_alph]
        identificators = [[str(num2alph(x, n)) 
                           for n in range(identificator_size)
                          ] 
                          for x in range(len_vocb)
                         ]
        # initialize table and iterable
        identificators_table = {}
        zip_id_voc = zip_longest(
            identificators, self.voc_structure, 
            fillvalue=None
        )
        # create dict identificator:word
        for idt, word in zip_id_voc:
            identificators_table[''.join(idt)] = word
        return identificators_table, identificator_size


    def _create_values_table(self):
        """Create table lexem_type->{identificator->vocabulary}, 
        and return it with sizes of an identificator as lexem_type->identificator_size"""
        # number of existing character, and returned dicts
        len_alph = len(self.alphabet)
        identificators_table = {k:{} for k in self.voc_values.keys()}
        identificators_sizes = {k:-1 for k in self.voc_values.keys()}

        for lexem_type, vocabulary in self.voc_values.items():
            # find number of different values that can be found, 
            #   and size of an identificator.
            len_vocb = len(vocabulary)
            identificators_sizes[lexem_type] = ceil(log(len_vocb, len_alph))
            # create list of possible identificators 
            num2alph = lambda x, n: self.alphabet[(x // len_alph**n) % len_alph]
            identificators = [[str(num2alph(x, n)) 
                               for n in range(identificators_sizes[lexem_type])
                              ] # this list is an identificator
                              for x in range(len_alph**identificators_sizes[lexem_type])
                             ] # this one is a list of identificator
            # initialize iterable
            zip_id_voc = zip_longest(
                identificators, vocabulary, 
                fillvalue=None
            )
            # create dict {identificator:word}
            for idt, voc in zip_id_voc:
                identificators_table[lexem_type][''.join(idt)] = voc

        # return all 
        return identificators_table, identificators_sizes


# PREDICATS ###################################################################
# ACCESSORS ###################################################################
# CONVERSION ##################################################################
# OPERATORS ###################################################################



