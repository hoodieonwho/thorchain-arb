from mnemonic import Mnemonic

def generate_mnemonic(language, filename):
    """Generate test_suite using user-specified language and save to local file
    :param language: language of test_suite words
    :type language: str
    :param filename: filename to save test_suite
    :type filename: str
    :returns: test_suite
    """
    words = Mnemonic(language).generate(strength=256)
    output = open(filename, "w+")
    output.write(words)
    output.close()
    return words

generate_mnemonic("english", "secret/real_mnemonic")