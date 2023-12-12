# -*- coding: utf-8 -*-
#########################
# IMPORTS               #
#########################
from accc.compiler import Compiler
from accc.langspec import python_spec

import random, time



#########################
# PRE-DECLARATIONS      #
#########################


#########################
# MAIN                  #
#########################
if __name__ == '__main__':
    def mutated(source_code, alphabet):
        """return an imperfect copy of source_code, modified at a random index"""
        source_code = list(source_code)
        index = random.randrange(0, len(source_code))
        old = source_code[index]
        while source_code[index] is old:
            source_code[index] = random.choice(alphabet)
        return ''.join(source_code)

    # create compiler
    alphabet = '01'
    cc  = Compiler(alphabet, python_spec,
                    ('parameter1', 'parameter2', 'parameter3', 'parameter4', 'int_value'),
                    ('have_that', 'is_this', 'have_many_things', 'know_that'),
                    ('do_that', 'say_this', 'do_it'),
                    ('>', '==', '<', 'is', '!='),
                  )

    # print source code, compile it, modify it, and loop ad vitam eternam
    source_code_size = 60
    source = ''.join((random.choice(alphabet) for _ in range(source_code_size)))
    while True:
        print(source)
        msource = mutated(source, alphabet)
        print(''.join([' ' if n == m else m for n, m in zip(source, msource)]))
        print(cc.compile(msource))
        print(source_code_size*'-')
        source = msource
        time.sleep(0.1)





