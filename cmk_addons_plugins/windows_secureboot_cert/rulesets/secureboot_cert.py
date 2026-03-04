#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.rulesets.v1 import Title, Help, Label
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
    SingleChoice,
    SingleChoiceElement,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, Topic, HostCondition


def _form_secureboot_cert() -> Dictionary:
    return Dictionary(
        title=Title("Secure Boot certificate status (Windows Server)"),
        elements={
            "enforce_secureboot": DictElement(
                parameter_form=BooleanChoice(
                    title=Title("Enforce Secure Boot enabled"),
                    help_text=Help("If enabled and Secure Boot is disabled, the check becomes CRIT."),
                    label=Label("enabled"),
                    prefill=DefaultValue(False),
                ),
            ),
            "require_2023": DictElement(
                parameter_form=SingleChoice(
                    title=Title("How to detect 2023 certificates"),
                    help_text=Help(
                        "any_2023 is robust and will work across most systems. "
                        "both_specific is stricter (requires DB Windows UEFI CA 2023 and KEK 2K CA 2023)."
                    ),
                    elements=[
                        SingleChoiceElement(name="any_2023", title=Title("At least one 2023 certificate detected (recommended)")),
                        SingleChoiceElement(name="both_specific", title=Title("Require both: DB Windows UEFI CA 2023 AND KEK 2K CA 2023 (stricter)")),
                    ],
                    prefill=DefaultValue("any_2023"),
                ),
            ),
            "warn_if_2011_present": DictElement(
                parameter_form=BooleanChoice(
                    title=Title("Warn if 2011 certificate is still present"),
                    help_text=Help("If enabled and a 2011 certificate is detected, add a WARN note."),
                    label=Label("enabled"),
                    prefill=DefaultValue(False),
                ),
            ),
        },
    )


rule_spec_secureboot_cert = CheckParameters(
    name="secureboot_cert",
    title=Title("Secure Boot certificate status (Windows Server)"),
    topic=Topic.WINDOWS,
    parameter_form=_form_secureboot_cert,
    condition=HostCondition(),
)
