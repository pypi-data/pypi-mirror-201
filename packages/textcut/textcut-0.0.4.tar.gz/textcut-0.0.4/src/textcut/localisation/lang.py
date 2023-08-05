import json
import os
import re

__all__ = ["rules", "LANG_FR"]

#: French language from France
LANG_FR = "fr-fr"


def rules(lang):
    """Get the cutting rules for a specific language. If the language variation is not found, only
    the main language will be used (`fr` in `fr-UK`, because `fr-UK` is not a thing). If the main
    language can't be found either, the function will fallback to `fr`.

    :param lang: ISO language code (e.g., en-UK, fr-FR, de, ...)
    :type lang: str

    :return: The cutting rules for that language
    :rtype: Rules

    :raises:
        FileNotFoundError: if language variation and top language files cannot be found.
    """

    lang = lang.lower()

    if lang not in (LANG_FR,):
        lang = LANG_FR

    here = os.path.dirname(__loader__.path)
    path = os.path.join(here, lang + ".json")
    if os.path.exists(path):
        return Rules(path)

    path = os.path.join(here, lang.split("-")[0] + ".json")
    if os.path.exists(path):
        return Rules(path)

    raise FileNotFoundError(f"Localisation file for '{lang}' could not be found")


class Rules:
    """Provide a convenient object to work with cutting rules used by textcut.
    The definition file is a JSON file.

    .. seealso::

        JSON schema file ``textcut/localisation/schema.json``
        Language files must comply with the JSON schema.

    :param filepath: The filepath to a JSON file listing the cutting rules
    :type filepath: str
    """

    def __init__(self, filepath):
        with open(filepath, "r") as fr:
            data = json.load(fr)

        self.lang    = data["lang"]
        self.after   = {}
        self.before  = {}
        self.default = data.get("default", 1)

        after  = data.get("after", [])
        before = data.get("before", [])

        for seqs in after:
            for seq in seqs["sequences"]:
                self.after[seq] = (float(seqs["probability"]), seqs.get("override", False))

        for seqs in before:
            for seq in seqs["sequences"]:
                self.before[seq] = (float(seqs["probability"]), seqs.get("override", False))


    def probabilities(self, text):
        """Compute the probability to cut before and after each character. The highest probability
        is kept, unless an overriding statement is met.

        :param text: The text to compute
        :type text: str

        :return: Probabilities to cut the text at each position.
        :rtype: Sequence[float]
        """

        length = len(text)
        if length == 0:
            return [1]

        proba_after  = [None] * length
        proba_before = [None] * length

        for seq, proba in self.after.items():
            x = self.__findall_position(seq, text, overlapping = True)

            for cut in self.__findall_position(seq, text, overlapping = True):
                position = min(length, cut[1])

                if proba_after[position - 1] is None or proba[1] is True:
                    proba_after[position - 1] = [*proba]
                else:
                    proba_after[position - 1][0] = max(proba[0], proba_after[position - 1][0])

        for seq, proba in self.before.items():
            for cut in self.__findall_position(seq, text, overlapping=True):
                position = max(0, cut[0])

                if proba_before[position] is None or proba[1] is True:
                    proba_before[position] = [*proba]
                else:
                    proba_before[position][0] = max(proba[0], proba_before[position][0])

        if proba_after[-1] is None:
            proba_after[-1] = [self.default, False]

        if proba_before[0] is None:
            proba_before[0] = [self.default, False]

        probabilities = [None] * (length + 1)
        for i in range(len(probabilities)):
            p_after  = [self.default, False]
            p_before = [self.default, False]

            if i > 0 and proba_after[i - 1] is not None:
                p_after = proba_after[i - 1]

            if i < (len(probabilities) - 1) and proba_before[i] is not None:
                p_before = proba_before[i]

            if not p_after[1] and not p_before[1]:
                probabilities[i] = max(p_after[0], p_before[0])
            else:
                probabilities[i] = max([x[0] for x in [p_after, p_before] if x[1]])

        return probabilities


    def __findall_position(self, pattern, text, overlapping=True):
        """Find all positions (beginning and end) of a pattern in text.

        :param pattern: The regex pattern to use with ``re.search``
        :type pattern: str

        :param text: The text to scan
        :type text: str

        :param overlapping: Whether to allow for overlapping positions or not; when set to
            ``False``, the returned positions are guaranteed to not overlap, defaults to ``True``
        :type overlapping: bool, optional

        :return: All the positions (beginning and end) in ``text`` where ``pattern`` was found.
        :rtype: Sequence[Tuple[int, int]]
        """

        cursor = 0
        while True:
            result = re.search(pattern, text[cursor:], re.MULTILINE)
            if result is None:
                break

            yield (result.start() + cursor, result.end() + cursor)

            if len(text[cursor:]) == 0:
                break

            if overlapping:
                cursor += result.start() + 1
            else:
                cursor += result.end()


    def print_proba(self, text):
        characters = "*+. "
        impossible = "×"

        probabilities = sorted(
                enumerate(self.probabilities(text)), key=lambda x: x[1],
                reverse = True)

        chars = [characters[-1]] * len(probabilities)
        chars[probabilities[0][0]] = characters[0]

        rank   = 0
        proba  = probabilities[0][1]
        legend = {characters[0]: proba}
        for i in range(1, len(probabilities)):
            if probabilities[i][1] < proba:
                rank += 1
                proba = probabilities[i][1]

                if rank >= len(characters):
                    break

                legend[characters[rank]] = proba

            chars[probabilities[i][0]] = characters[rank]

        for i, p in probabilities:
            if p == 0:
                chars[i] = impossible
                legend[impossible] = 0

        print(" " + text)
        print("".join(chars))

        for c, p in legend.items():
            print(f"{c}: {p:6.2%}")
