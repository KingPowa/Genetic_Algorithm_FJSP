from parser import *
from ga_handler import GAHandler
# problem = parseFile("Dataset/test.fjs")
problem = parseFile("Dataset/Brandimarte_Data/Text/Mk02.fjs")
handler = GAHandler(problem)
# handler.runBroad(120, 2000, 5, 24)
# handler.runConditional(120, 2000, 5, 24)
handler.runMixed02(120, 2000, 5, 24)

# problem = parseFile("Dataset/Brandimarte_Data/Text/Mk02.fjs")
# # handler = GAHandler(problem)
# # handler.runBroad(120, 2000, 5, 24)


