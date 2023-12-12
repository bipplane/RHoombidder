# -*- coding: utf-8 -*-
#########################
#       DNACOMPILER     #
#########################


#########################
# IMPORTS               #
#########################
from accc.compiler import Compiler



#########################
# PRE-DECLARATIONS      #
#########################



#########################
# DNACOMPILER CLASS     #
#########################
class DNACompiler(Compiler):
    """
    Compiler specialized in DNA: vocabulary is 'ATGC'.
    """
    def __init__(self, target_language_spec, comparables, predicats, actions, operators):
        """"""
        super().__init__('ATGC', target_language_spec, comparables, predicats, actions, operators)




#########################
# FUNCTIONS             #
#########################
if __name__ == '__main__':
    import random, time
    from accc.langspec import python as python_spec

            
    def mutated(dna, mutation_rate=0.1):
        new_dna = ''
        for nuc in dna:
            if random.random() < mutation_rate:
                new_dna += random.choice(dc.alphabet)
            else:
                new_dna += nuc
        return new_dna


    dc = DNACompiler(python_spec,
                     ('temperature',),
                     ('haveNeighbors',),
                     ('die', 'duplicate'),
                     ('>', '==', '<')
                    )

    # print source code, compile it, modify it, and loop ad vitam eternam
    dna = ''.join((random.choice(dc.alphabet) for _ in range(40)))
    while True:
        print(dna)
        mdna = mutated(dna)
        print(''.join([' ' if n == m else '!' for n, m in zip(dna, mdna)]))
        print(dc.compile(mdna))
        print(dc.header(dna), dc.structure(dna), dc.values(dna), sep='|', end='\n------------\n\n\n\n')

        time.sleep(0.4)








