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


def amm_output(i_amount, i_depth, o_depth):
    return i_amount * i_depth * o_depth / (i_amount + i_depth) ** 2
    # outbound fee


def doubleswap_output(input_amount, pool1_data, pool2_data):
    swap1_out = amm_output(input_amount, int(pool1_data["balance_asset"]), int(pool1_data["balance_rune"]))
    swap2_out = amm_output(swap1_out, int(pool2_data["balance_rune"]), int(pool2_data["balance_asset"]))
    return swap2_out
    # outbound fee