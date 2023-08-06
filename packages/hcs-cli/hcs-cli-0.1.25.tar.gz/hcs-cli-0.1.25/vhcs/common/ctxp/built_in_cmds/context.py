import click
import vhcs.common.ctxp as ctxp


@click.group(cls=ctxp.cli_processor.LazyGroup)
def context():
    """Commands for context, for the current profile."""


@context.command()
def list():
    """List all context item names, for the current profile."""
    return ctxp.context.list()


@context.command()
@click.argument("name")
@click.argument("key", required=False)
def get(name: str, key: str):
    """Get data of a specific context object, for the current profile."""
    data = ctxp.context.get(name)

    if key is None:
        return data
    if data is None:
        return None
    return data.get(key)


@context.command()
@click.argument("name")
@click.argument("key_value")  #'key value pair, example: k1=v1'
def set(name: str, key_value: str):
    """Set a context object by name, for the current profile."""
    parts = key_value.split("=")
    if len(parts) != 2:
        ctxp.panic("Invalid KEY_VALUE format. Valid example: key1=value1")
    k, v = parts
    data = ctxp.context.get(name, default={})
    data[k] = v
    ctxp.context.set(name, data)


@context.command()
@click.argument("name")
def delete(name: str):
    """Delete a context object by name, for the current profile."""
    ctxp.context.delete(name)


@context.command()
def clear():
    """Delete all context objects, for the current profile."""
    ctxp.context.clear()
