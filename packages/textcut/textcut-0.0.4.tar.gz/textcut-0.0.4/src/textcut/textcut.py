import math
import statistics
from . import localisation

class TextCut:
    """Wrap a text based on more advanced probabilities, depending on the context of the text. The
    probabilities depends on the language.

    :param language: The ISO language code, defaults to french (fr-FR)
    :type language: str, optional

    :param width: The maximal width of each line, defaults to 100
    :type width: int, optional

    :param tolerance: How short the wrapper is tolerant to shorter string than requested. High
        value (>5) basically means the wrapper does not care about the length of the results, but
        will look for the best cutting position. For value around 0.5 to 1.0, the wrapper will
        prefer longer lines (closer to the requested width), but may occasionnaly choose a shorter
        line, if it gives a good compromise. Low value (<0.1) will always prefer long lines, even
        if it means cutting between words instead of paragraph, or even within words. Defaults
        to 0.5
    :type tolerance: float, optional

    :param trim: Trim white spaces for each line, defaults to True
    :type trim: bool, optional

    :param len_func: A function used to determine the length of the string, to accomodate for
        non-linear quantifications. Example: ``lambda x: sum([1 for c in x if c != " "])`` will
        count non-space characters only. Defaults to standard ``len``.
    :type len_func: Callable, optional

    :param normalise: Try to minimise the difference in character length between the sentences,
        defaults to False.
    :type normalise: boolean, optional
    """
    def __init__(self, language=localisation.LANG_FR, width=100, tolerance=0.5, trim=True,
                 len_func=len, normalise=False):
        if width <= 0:
            raise ValueError(f"Invalid width value: {width}")

        self.language  = language
        self.width     = width
        self.tolerance = tolerance
        self.trim      = trim
        self.len_func  = len_func
        self.normalise = normalise

        self.rules     = localisation.rules(language)


    def wrap(self, text):
        """Wrap the text using the parameters defined in the constructor.

        :param text: The text to wrap
        :type text: str

        :return: One or more lines of no more than ``width``-character long.
        :rtype: Sequence[str]
        """

        if self.normalise:
            return self.__normalised_wrap(text)

        probabilities = self.rules.probabilities(text)
        lines = []

        while self.len_func(text) > self.width:
            max_i = 0
            max_p = 0
            i     = 1

            while self.len_func(text[:i]) < self.width + 1:
                x = i / self.width
                p = probabilities[i] * math.exp(-(((x - 1) / self.tolerance) ** 2))

                if p >= max_p:
                    max_i = i
                    max_p = p

                i += 1

            lines += [text[:max_i]]
            text = text[max_i:]
            probabilities = probabilities[max_i:]

            if self.trim:
                lines[-1] = lines[-1].strip()

        lines += [text]
        if self.trim:
            lines[-1] = lines[-1].strip()

        return lines


    def fill(self, text):
        """Produces a string print-ready using ``\\n`` to collapse the lines. This method is a
        shortcut for ``"\\n".join(wrap(text))``.

        :param text: The text to wrap
        :type text: str

        :return: The wrapped lines glued together with a linefeed character (``\\n``).
        :rtype: str
        """

        return "\n".join(self.wrap(text))


    def __normalised_wrap(self, text):
        """Wrap the text using the parameters defined in the constructor.
        Make an attempt to normalise the text length for each part. The algorithm
        will explore neighbouring values of ``width`` and ``tolerance`` to pick
        the results yielding the minimum standard deviation of text length.

        The width will be explored 15% below the requested value.
        The tolerance will be explored 25% around the requested value (51 values).

        :param text: The text to wrap
        :type text: str

        :return: One or more lines of no more than ``width``-character long.
        :rtype: Sequence[str]
        """

        self.normalise = False
        defwrap = self.wrap(text)

        if len(defwrap) == 1:
            self.normalise = True
            return defwrap

        ini_width     = self.width
        ini_tolerance = self.tolerance

        min_width     = int(round(0.85 * self.width))
        min_tolerance = 0.25 * self.tolerance
        max_tolerance = 1.25 * self.tolerance
        num_tolerance = 51

        best_std      = statistics.stdev([len(x) for x in defwrap])
        best_out      = defwrap

        for w in range(min_width, ini_width+1):
            self.width = w

            for t in range(0, num_tolerance):
                self.tolerance = min_tolerance + (max_tolerance - min_tolerance) * t / (num_tolerance - 1)

                exp_wrap = self.wrap(text)
                exp_std  = statistics.stdev([len(x) for x in exp_wrap])

                if exp_std < best_std:
                    best_std = exp_std
                    best_out = exp_wrap

        self.width     = ini_width
        self.tolerance = ini_tolerance
        self.normalise = True

        return best_out
