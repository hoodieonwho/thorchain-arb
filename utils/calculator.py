def clp(inputAmount, inputDepth, outputDepth):
    outputAmount = inputAmount * inputDepth * outputDepth / (inputAmount + inputDepth)**2
    return outputAmount


def divide_conquer(slice, inputA, DepthA, DepthB):
    outputB = 0
    count = 0
    slicedunit = inputA/slice
    while count < slice:
        piece = clp(slicedunit,DepthA+slicedunit*count,DepthB-outputB)
        outputB += piece
        count += 1
    return outputB


def optimal(inputAmount, inputDepth, outputDepth, fee_output, round=4):
    no_strategy = clp(inputAmount, inputDepth, outputDepth) - fee_output
    strategy = [1, no_strategy]
    for x in reversed(range(2,round)):
        output = divide_conquer(slice=x, inputA=inputAmount, DepthA=inputDepth, DepthB=outputDepth) - fee_output * x
        if output > strategy[1]:
            strategy = [x, output]
    return no_strategy, strategy


def slip(inputAmount, inputDepth, outputDepth):
    slip = inputAmount ** 2 * outputDepth / (inputAmount + inputDepth) ** 2
    return slip

