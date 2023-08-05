"""Obligations module"""

import ssl
import json
import urllib.request as req
from urllib.request import Request, HTTPError

import re
from logging import Logger
from pathlib import Path

REGEX_EGN = r"^[0-9]{2}[0,1,2,4][0-9][0-9]{2}[0-9]{4}$"
REGEX_DRIVING_LICENSE = r"^[0-9]{9}$"

KAT_OBLIGATIONS_URL = "https://e-uslugi.mvr.bg/api/Obligations/AND?mode=1&obligedPersonIdent={egn}&drivingLicenceNumber={license_number}"


class KatPersonDetails:
    """Holds the person data needed to make the obligations check."""

    def __init__(self, person_egn: str, driving_license_number: str) -> None:
        self.person_egn = person_egn
        self.driving_license_number = driving_license_number
        self.__validate()

    def __validate(self):
        if self.person_egn is None:
            raise ValueError("EGN Missing")
        else:
            egn_match = re.search(REGEX_EGN, self.person_egn)
            if egn_match is None:
                raise ValueError("EGN is not valid")

        if self.driving_license_number is None:
            raise ValueError("Driving License Number missing")
        else:
            license_match = re.search(
                REGEX_DRIVING_LICENSE, self.driving_license_number
            )
            if license_match is None:
                raise ValueError("Driving License Number not valid")


class KatObligationsDetails:
    """The obligations response object."""

    def __init__(self, has_obligations: bool) -> None:
        self.has_obligations = has_obligations


class KatError(Exception):
    """Error wrapper"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def check_obligations(
    person: KatPersonDetails, logger: Logger = None
) -> KatObligationsDetails:
    """
    Calls the public URL to check if an user has any obligations.

    :param person_egn: EGN of the person
    :param driving_license_number: Driver License Number

    """
    try:
        url = KAT_OBLIGATIONS_URL.format(
            egn=person.person_egn, license_number=person.driving_license_number
        )
        headers = {
            "content-type": "application/json",
        }

        if logger is not None:
            logger.debug("KAT Url called: %s", url)

        cafile_path = f"{Path(__file__).parent}/cert/chain_2024_03_19.pem"

        resp = req.urlopen(
            url=Request(url, headers=headers),
            timeout=10,
            context=ssl.create_default_context(cafile=cafile_path),
        )

        data = json.loads(resp.read().decode())

    except HTTPError as ex:
        if logger is not None:
            logger.warning("KAT Bulgaria HTTP call failed: %e", str(ex))

        # TODO: Validate for code=GL_00038_E
        # TODO: Validate for code=GL_UNDELIVERED_AND_UNPAID_DEBTS_E

        raise KatError(f"KAT website returned an error: {str(ex)}") from ex

    except TimeoutError as ex:
        if logger is not None:
            logger.info("KAT Bulgaria HTTP call TIMEOUT: %e", str(ex))

        raise KatError("KAT website took too long to respond.") from ex

    if "hasNonHandedSlip" not in data:
        raise KatError("KAT Bulgaria returned a malformed response")

    return KatObligationsDetails(data["hasNonHandedSlip"])
