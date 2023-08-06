
def longest_common_sequence(s1: str, s2: str) -> int:
    """
    문자열 A, B의 최장 공통 문자열 길이

    :param s1: 문자열 A
    :type s1: str
    :param s2: 문자열 B
    :type s2: str
    :return: 최장 공통 문자열 길이
    :rtype: int
    :Example:
        >>> longest_common_sequence('a', 'b')
        0
        >>> longest_common_sequence('aa', 'ba')
        1
        >>> longest_common_sequence('aa', 'aba')
        2
        >>> longest_common_sequence('aa', 'ab')
        1
        >>> longest_common_sequence('abcd', 'ababadcd')
        4
        >>> longest_common_sequence('ababa', 'ababcd')
        4
        >>> longest_common_sequence('서울강남초등학교', '서울강남 사립초교')
        6
    """
    if not isinstance(s1, str):
        s1 = str(s1 or '')
    if not isinstance(s2, str):
        s2 = str(s2 or '')

    len1 = len(s1)
    len2 = len(s2)

    if len1 == 0 or len2 == 0:
        return 0

    if len1 > len2:
        s1, s2 = s2, s1
        len1, len2 = len2, len1

    DP = [[0] * len1 for _ in range(2)]
    idx = 0

    for i in range(len2):
        idx = i % 2
        for j in range(len1):
            left = DP[idx][j - 1] if j > 0 else 0
            up = DP[1 - idx][j] if i > 0 else 0
            diag = DP[1 - idx][j - 1] if i > 0 and j > 0 else 0

            DP[idx][j] = 1 + diag if s2[i] == s1[j] else max(left, up)

    return DP[idx][len1 - 1]


class SegmentTree:
    # todo
    pass


class SegmentTreeLazyPropagation:
    # todo
    pass


class FenwickTree:
    # todo
    pass
