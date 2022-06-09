def comb(N, k, exact=False, repetition=False, legacy=True):
    """scipy is not compatible with pypy

	So I have copy pasted this func here to avoid the import
	https://github.com/scipy/scipy/blob/main/scipy/special/_basic.py#L2163-L2251

	The number of combinations of N things taken k at a time.
    This is often expressed as "N choose k".
    Parameters
    ----------
    N : int, ndarray
        Number of things.
    k : int, ndarray
        Number of elements taken.
    exact : bool, optional
        For integers, if `exact` is False, then floating point precision is
        used, otherwise the result is computed exactly. For non-integers, if
        `exact` is True, the inputs are currently cast to integers, though
        this behavior is deprecated (see below).
    repetition : bool, optional
        If `repetition` is True, then the number of combinations with
        repetition is computed.
    legacy : bool, optional
        If `legacy` is True and `exact` is True, then non-integral arguments
        are cast to ints; if `legacy` is False, the result for non-integral
        arguments is unaffected by the value of `exact`.
        .. deprecated:: 1.9.0
            Non-integer arguments are currently being cast to integers when
            `exact=True`. This behaviour is deprecated and the default will
            change to avoid the cast in SciPy 1.11.0. To opt into the future
            behavior set `legacy=False`. If you want to keep the
            argument-casting but silence this warning, cast your inputs
            directly, e.g. ``comb(int(your_N), int(your_k), exact=True)``.
    Returns
    -------
    val : int, float, ndarray
        The total number of combinations.
    See Also
    --------
    binom : Binomial coefficient considered as a function of two real
            variables.
    Notes
    -----
    - Array arguments accepted only for exact=False case.
    - If N < 0, or k < 0, then 0 is returned.
    - If k > N and repetition=False, then 0 is returned.
    Examples
    --------
    >>> from scipy.special import comb
    >>> k = np.array([3, 4])
    >>> n = np.array([10, 10])
    >>> comb(n, k, exact=False)
    array([ 120.,  210.])
    >>> comb(10, 3, exact=True)
    120
    >>> comb(10, 3, exact=True, repetition=True)
    220
    """
    if repetition:
        return comb(N + k - 1, k, exact, legacy=legacy)
    if exact:
        if int(N) != N or int(k) != k:
            if legacy:
                warnings.warn(
                    "Non-integer arguments are currently being cast to "
                    "integers when exact=True. This behaviour is "
                    "deprecated and the default will change to avoid the cast "
                    "in SciPy 1.11.0. To opt into the future behavior set "
                    "legacy=False. If you want to keep the argument-casting "
                    "but silence this warning, cast your inputs directly, "
                    "e.g. comb(int(your_N), int(your_k), exact=True).",
                    DeprecationWarning, stacklevel=2
                )
            else:
                return comb(N, k)
        # _comb_int casts inputs to integers
        return _comb_int(N, k)
    else:
        k, N = asarray(k), asarray(N)
        cond = (k <= N) & (N >= 0) & (k >= 0)
        vals = binom(N, k)
        if isinstance(vals, np.ndarray):
            vals[~cond] = 0
        elif not cond:
            vals = np.float64(0)
        return vals
