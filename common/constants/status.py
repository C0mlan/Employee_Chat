class Status:
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DELETED = "DELETED"
    TERMINATED = "TERMINATED"
    
    CHOICES = [
        (ACTIVE, "Active"),
        (SUSPENDED, "Suspended"),
        (DELETED, "Deleted"),
        (TERMINATED, "Terminated")]