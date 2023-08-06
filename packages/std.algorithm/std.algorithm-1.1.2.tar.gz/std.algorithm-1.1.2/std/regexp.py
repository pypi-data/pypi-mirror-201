
def not_any(regex):
    return f"(?!(?:{regex}))\S+"

if __name__ == '__main__':
    ...