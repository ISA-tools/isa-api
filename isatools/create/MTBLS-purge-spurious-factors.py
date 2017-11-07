from isatools.utils import IsaTabFixer
import os
import re


def main():
    fixer = IsaTabFixer('/Users/Philippe/Downloads/ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/MTBLS81/s_Study id.txt')

    this_factor="Age at sacrifice"

    fixer.fix_factor(this_factor)  # fixes by moving factor to charac

    # spurious_factors = "factor: Age at sacrifice"
    #
    # factornames = []
    # factornames = spurious_factors.split("factor: ")
    #
    # for element in factornames:
    #
    #     this_factor = element.strip()
    #     this_factor = re.sub(";","", this_factor)
    #     this_factor = this_factor.strip()
    #     print(this_factor)


if __name__ == '__main__':
    main()