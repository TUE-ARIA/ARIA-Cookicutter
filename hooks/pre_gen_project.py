#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Configuration tasks to be run before the template has been generated."""

import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("pre_gen_project")

assert "\\" not in "{{ cookiecutter.author_name }}", "Don't include backslashes in author name."

PROJECT_SLUG_REGEX = r"^[a-z][_a-z0-9]+$"

# Regular expression to check for a valid email address — based on the HTML5 standard
# (https://html.spec.whatwg.org/multipage/input.html#valid-e-mail-address). This is
# more restrictive than the RFC standard; see the comments in this SO answer for
# further information: https://stackoverflow.com/a/201378
REGEX_EMAIL_ADDRESS = (
    r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
)


def check_valid_email_address_format(email: str) -> None:
    """Check that an email address is of a valid format using regular expressions.
    `Uses a regular expression pattern based on the HTML5 standard for email address
    format <https://html.spec.whatwg.org/multipage/input.html#valid-e-mail-address>`_.
    Args:
        email: An email address to validate.
    Returns:
        None - raises an `AssertionError` if `email` is not a valid email address
        format.
    """
    assert bool(
        re.fullmatch(REGEX_EMAIL_ADDRESS, email),
    ), f"Invalid email address supplied: {email}"


if __name__ == "__main__":

    module_name = "{{cookiecutter.project_slug}}"

    if not re.match(PROJECT_SLUG_REGEX, module_name):
        link = "https://www.python.org/dev/peps/pep-0008/#package-and-module-names"
        logger.error("Module name should be pep-8 compliant.")
        logger.error("  More info: {}".format(link))

        # exits with status 1 to indicate failure
        sys.exit(1)

    # Check the format of the contact email address supplied is a valid one
    check_valid_email_address_format("{{ cookiecutter.author_email }}")

# EOF
