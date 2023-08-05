"""
2022, May 12
"""

from ..core.variable import *
import fonsim.constants.norm as cnorm

terminal_fluidic = [Variable('pressure', 'across', cnorm.pressure_atmospheric),
                    Variable('massflow', 'through', 0)]
