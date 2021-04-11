class InvaildDomain(Exception):
    def __init__(self, domain):
        self.text = f"`@{domain}`은 사용할수 없습니다."
    def __str__(self):
        return self.text

class InvaildInput(Exception):
    def __init__(self, input):
        self.text = f"`{input}` 은 올바르지 않은 이메일입니다."
    def __str__(self):
        return self.text

class AlreadyExsistingEmail(Exception):
    def __init__(self, email):
        self.text = f"`{email}`은 이미 사용중입니다. 다른 이메일 주소를 사용해 주세요."
    def __str__(self):
        return self.text

class AlreadyExsistingUser(Exception):
    def __init__(self, userid, email):
        self.text = f"<@{userid}> 님은 이미 등록된 이메일 주소({email})가 있습니다."
    def __str__(self):
        return self.text