def lnTaylor(x, eps):
    """Calculate ln(1+x) as Taylor siries, while step < eps

    Return List 0:sum, 1:number of iteretion
    """
    sum = 0.
    for n in range(1, 501):
        step = pow(-1, n - 1) * pow(x, n) / n
        sum += step
        if abs(step) < eps :
            return (sum, n)
    return [sum, n]