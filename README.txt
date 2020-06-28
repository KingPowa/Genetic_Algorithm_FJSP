To execute, uses the declared function in ga_handler

handler = GAHandler(problem) # Creates a handler for the problem
handler.runConditional(number_of_individuals, num_of_generations, iterations, max_reachable) # For executing Conditional
handler.runBroad(number_of_individuals, num_of_generations, iterations, max_reachable) # For executing Broad
handler.runMixed1(number_of_individuals, num_of_generations, iterations, max_reachable) # For executing a specific algorithm for MK01
handler.runMixed2(number_of_individuals, num_of_generations, iterations, max_reachable) # For executing a specific algorithm for MK02
