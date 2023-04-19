class UserState:
    active = "active"
    blocked = "blocked"
    waiting = "waiting"
    
    CHOICES = (
        (active, "active"),
        (blocked, "blocked"),
        (waiting, "waiting"),
    )