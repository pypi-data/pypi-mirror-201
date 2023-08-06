from preservationdatabase.models import (
    CarinianaPreservation,
    ClockssPreservation,
    HathiPreservation,
    InternetArchivePreservation,
    InternetArchiveItem,
    LockssPreservation,
    OculScholarsPortalPreservation,
    PKPPreservation,
    PorticoPreservation,
)

archives = {
    "cariniana": CarinianaPreservation,
    "clockss": ClockssPreservation,
    "hathitrust": HathiPreservation,
    "internet_archive": InternetArchivePreservation,
    "internet_archive_scholar": InternetArchiveItem,
    "lockss": LockssPreservation,
    "pkp": PKPPreservation,
    "portico": PorticoPreservation,
    "ocul": OculScholarsPortalPreservation,
}
