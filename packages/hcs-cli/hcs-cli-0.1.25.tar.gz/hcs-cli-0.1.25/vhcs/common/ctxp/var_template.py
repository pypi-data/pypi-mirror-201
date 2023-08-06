import re
import logging
from . import jsondot
from .jsondot import dotdict
from . import profile
from . import context

log = logging.getLogger(__name__)

_variables = None


def _vars() -> dotdict:
    global _variables
    _variables = context.get(".variables")
    return _variables


def _save():
    context.save(".variables", _variables)


def set(name: str, value: any):
    variables = _vars()
    if name in variables:
        existing = variables.get(name)
        if existing == value:
            return
        log.debug(f"Updating [{name}] from [{existing}] to [{value}]")
    else:
        log.debug(f"Setting [{name}] to [{value}]")
    variables[name] = value
    _save()


def delete(name: str):
    variables = _vars()
    if name in variables:
        del variables[name]
        _save()


def get(name: str):
    variables = _vars()
    v = None
    if name in variables:
        v = variables[name]
    else:
        plain_profile = _get_plain_profile()
        if name in plain_profile:
            v = plain_profile[name]
        else:
            raise Exception("Variable not found in context and profile: " + name)
    return v


def apply(template: str | dict, additional_vars: dict = None):
    mapping = _vars().copy()
    if additional_vars:
        mapping |= additional_vars

    # merge profile
    mapping |= _get_plain_profile()

    # The Python default Template.substitute has too many limitations...
    def substitute(text: str):
        pattern = re.compile(".*\${(.+?)}.*")
        while True:
            m = pattern.match(text)
            if not m:
                break
            name = m.group(1)
            val = str(get(name))
            text = text.replace("${" + name + "}", val)
        return text

    def apply_impl(target):
        t = type(target)
        try:
            if t is str:
                target = substitute(target)
            elif t is dict:
                for k, v in target.items():
                    target[k] = apply_impl(v)
            elif t is list:
                for i in range(len(target)):
                    target[i] = apply_impl(target[i])
            else:
                pass
            return target
        except KeyError as e:
            raise Exception("Variable not defined in context") from e


def _get_plain_profile():
    global _plain_profile
    if _plain_profile is None:
        _plain_profile = {}
        data = profile.plain()
        for k in data:
            _plain_profile["profile." + k] = data[k]
    return _plain_profile


def load_template(name: str):
    tmpl = jsondot.load(name)
    return apply(tmpl)
