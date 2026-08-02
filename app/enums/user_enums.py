from enum import Enum


class UserAnketaStatus(Enum):
    """*Review status of a user anketa (profile questionnaire).*"""

    pending = 'PENDING'
    approved = 'APPROVED'
    rejected = 'REJECTED'
