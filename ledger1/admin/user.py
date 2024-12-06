from dataclasses import dataclass

@dataclass
class User:
    user_id: int | str = "new"
    user_name: str = ""
    email: str = ""
    user_pass: str = ""
    user_role: str = "user"
    entities: str = ['example']
    entity: str = "example"
    active: bool = True
