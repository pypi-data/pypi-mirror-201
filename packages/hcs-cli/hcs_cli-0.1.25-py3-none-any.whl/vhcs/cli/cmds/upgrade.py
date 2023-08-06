import click
import subprocess
import sys


@click.group(invoke_without_command=True)
def upgrade():
    """Upgrade hcs-cli."""
    cmd = f"pip3 install -U hcs-cli --upgrade-strategy eager --no-cache-dir"
    p = subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr, text=False, shell=True, check=False)
    return p.returncode
