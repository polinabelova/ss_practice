class AnnouncmentState:

    draft = 'draft'
    moderate = "moderate"
    rejected = "rejected"
    active = 'active'

    CHOICES = (
        (draft, 'draft'),
        (moderate, "moderate"),
        (rejected, "rejected"),
        (active, 'active'),
    )
