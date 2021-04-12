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

class AlreadyExistingEmail(Exception):
    def __init__(self, email):
        self.text = f"`{email}`은 이미 사용중입니다. 다른 이메일 주소를 사용해 주세요."
    def __str__(self):
        return self.text

class AlreadyExistingUser(Exception):
    def __init__(self, userid, email):
        self.text = f"<@{userid}> 님은 이미 등록된 이메일 주소({email})가 있습니다."
    def __str__(self):
        return self.text

class BlankInputReceived(Exception):
    def __init__(self):
        self.text = "비어있는 입력은 허용되지 않습니다. 이메일 주소 형태로 입력해 주세요."
    def __str__(self):
        return self.text

class NotExistingUser(Exception):
    def __init__(self):
        self.text = "이 명령어를 사용하려면 이메일 주소가 있어야 합니다. `/createmail`명령어로 이메일을 생성하세요."
    def __str__(self):
        return self.text