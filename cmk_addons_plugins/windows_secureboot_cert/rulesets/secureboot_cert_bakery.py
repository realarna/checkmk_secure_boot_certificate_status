#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    Dictionary,
    DictElement,
    FixedValue,
)
from cmk.rulesets.v1.rule_specs import AgentConfig, Topic


def _parameter_valuespec_secureboot_cert_bakery() -> Dictionary:
    return Dictionary(
        title=Title("Agent plugin deployment"),
        help_text=Help("Deploys the Windows agent plugin secureboot_cert.ps1 via the Agent Bakery."),
        elements={
            "deployment": DictElement(
                parameter_form=CascadingSingleChoice(
                    title=Title("Deployment"),
                    help_text=Help("Choose whether the agent plugin should be deployed to the host."),
                    elements=[
                        CascadingSingleChoiceElement(
                            name="deploy",
                            title=Title("Deploy the plugin"),
                            parameter_form=FixedValue(
                                value=True,
                                title=Title("Deploy"),
                            ),
                        ),
                        CascadingSingleChoiceElement(
                            name="do_not_deploy",
                            title=Title("Do not deploy the plugin"),
                            parameter_form=FixedValue(
                                value=False,
                                title=Title("Do not deploy"),
                            ),
                        ),
                    ],
                    prefill="deploy",
                ),
            ),
        },
    )


rule_spec_agent_secureboot_cert = AgentConfig(
    title=Title("Secure Boot certificate agent plugin (Windows)"),
    topic=Topic.WINDOWS,
    name="secureboot_cert",
    parameter_form=_parameter_valuespec_secureboot_cert_bakery,
)
