import pytest

from gpp.algorithms import longest_common_sequence


@pytest.mark.parametrize('s1, s2, expected', [
    ('', '', 0),  #
    (None, None, 0),  #
    (1, '1', 1),  #
    ('a', 'b', 0),  #
    ('aa', 'ba', 1),  # a
    ('aa', 'aba', 2),  # aa
    ('aba', 'aa', 2),  # aa
    ('aa', 'ab', 1),  # a
    ('abcd', 'ababadcd', 4),  # abcd
    ('ababa', 'ababcd', 4),  # abab
    ('서울강남초등학교', '서울강남 사립초교', 6)  # 서울강남초교
])
def test_algorithms_longest_common_sequence(s1, s2, expected):
    ##########################################################
    # precondition

    ##########################################################
    # call function

    ##########################################################
    # assertion
    assert longest_common_sequence(s1, s2) == expected
