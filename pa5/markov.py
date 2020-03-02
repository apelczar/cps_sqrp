'''
CAPP 30122 W'20: Markov models and hash tables

YOUR NAME HERE
'''

import sys
import math
import hash_table

HASH_CELLS = 57


class Markov:

    def __init__(self, k, s):
        '''
        Construct a new k-order Markov model using the statistics of string "s"
        '''
        ### YOUR CODE HERE ###
        pass

    def log_probability(self, s):
        '''
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.
        '''
        ### YOUR CODE HERE ###
        pass


def identify_speaker(speaker_a, speaker_b, unknown_speech, k):
    '''
    Given sample text from two speakers, and text from an unidentified speaker,
    return a tuple with the *normalized* log probabilities of each of the
    speakers uttering that text under a "k" order character-based Markov model,
    and a conclusion of which speaker uttered the unidentified text
    based on the two probabilities.
    '''
    ### YOUR CODE HERE ###
    return (None, None, None)


def print_results(res_tuple):
    '''
    Given a tuple from identify_speaker, print formatted results to the screen
    '''
    (likelihood1, likelihood2, conclusion) = res_tuple

    print("Speaker A: " + str(likelihood1))
    print("Speaker B: " + str(likelihood2))

    print("")

    print("Conclusion: Speaker " + conclusion + " is most likely")


def go():
    '''
    Interprets command line arguments and runs the Markov analysis.
    Useful for hand testing.
    '''
    num_args = len(sys.argv)

    if num_args != 5:
        print("usage: python3 " + sys.argv[0] + " <file name for speaker A> " +
              "<file name for speaker B>\n  <file name of text to identify> " +
              "<order>")
        sys.exit(0)

    with open(sys.argv[1], "rU") as file1:
        speech1 = file1.read()

    with open(sys.argv[2], "rU") as file2:
        speech2 = file2.read()

    with open(sys.argv[3], "rU") as file3:
        speech3 = file3.read()

    res_tuple = identify_speaker(speech1, speech2, speech3, int(sys.argv[4]))

    print_results(res_tuple)

if __name__ == "__main__":
    go()
