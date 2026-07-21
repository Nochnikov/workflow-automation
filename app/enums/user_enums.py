from enum import Enum


class UserAnketaStatus(Enum):
    pending = 'PENDING'
    approved = 'APPROVED'
    rejected = 'REJECTED'
