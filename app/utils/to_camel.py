def to_camel(string: str) -> str:
    """snake_case를 camelCase로 변환합니다."""
    words = string.split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:])