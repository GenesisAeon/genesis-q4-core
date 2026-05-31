"""CLI for genesis-q4-core: genesis-q4 <command> [options]."""

from __future__ import annotations

try:
    import typer
    from rich.console import Console
    from rich.table import Table
except ImportError:
    raise ImportError(
        "CLI requires 'typer' and 'rich': pip install 'genesis-q4-core[cli]'"
    )

from genesis_q4.gray_code import GrayCode
from genesis_q4.serializer import state_to_dict
from genesis_q4.state import Q4State
from genesis_q4.tesseract import Tesseract
from genesis_q4.transitions import InvalidTransitionError, Q4TransitionValidator

app = typer.Typer(help="genesis-q4: 16-state Q4 space with Gray-Code and Tesseract topology.")
console = Console()


@app.command()
def state(
    id: int = typer.Option(..., "--id", help="State ID 0..15"),
) -> None:
    """Show details for a single Q4 state."""
    s = Q4State.from_id(id)
    t = Table(title=f"Q4 State {s.binary} (ID={s.id})")
    t.add_column("Property")
    t.add_column("Value")
    for k, v in state_to_dict(s).items():
        t.add_row(str(k), str(v))
    console.print(t)


@app.command()
def path(
    from_: int = typer.Option(..., "--from", help="Source state ID"),
    to: int = typer.Option(..., "--to", help="Target state ID"),
) -> None:
    """Find the shortest Gray-Code path between two states."""
    tess = Tesseract()
    ids = tess.shortest_gray_path(from_, to)
    states = [Q4State.from_id(i) for i in ids]
    console.print(f"[bold]Shortest Gray path:[/bold] {from_} → {to}  ({len(ids)-1} transitions)")
    for i, s in enumerate(states):
        prefix = "START" if i == 0 else ("END " if i == len(states) - 1 else f"  {i}  ")
        console.print(f"  {prefix}  {s.binary}  (id={s.id})")


@app.command()
def validate(
    from_: int = typer.Option(..., "--from", help="Source state ID"),
    to: int = typer.Option(..., "--to", help="Target state ID"),
) -> None:
    """Validate a Q4 state transition (Gray-Code policy gate)."""
    v = Q4TransitionValidator()
    try:
        v.validate(from_, to)
        console.print(f"[green]VALID[/green]  {from_:04b} → {to:04b}  (Hamming distance = 1)")
    except InvalidTransitionError as e:
        console.print(f"[red]INVALID[/red]  {e}")
        suggestion = v.suggest_path(from_, to)
        console.print(f"[yellow]Suggested path:[/yellow] {' → '.join(f'{i:04b}' for i in suggestion)}")


@app.command()
def visualize(
    format: str = typer.Option("mermaid", "--format", help="Output format: mermaid or json"),
) -> None:
    """Visualize the Q4 tesseract topology."""
    tess = Tesseract()
    if format == "mermaid":
        console.print(tess.export_mermaid())
    elif format == "json":
        import json
        console.print(json.dumps(tess.export_json(), indent=2))
    else:
        console.print(f"[red]Unknown format: {format}. Use 'mermaid' or 'json'.[/red]")


@app.command("list-states")
def list_states() -> None:
    """List all 16 Q4 states with their properties."""
    t = Table(title="All 16 Q4 States  (16 states = 4 bit, H = log₂(16) = 4 bit)")
    for col in ("ID", "Binary", "C", "R", "E", "P", "Gray ID", "Entropy (bit)"):
        t.add_column(col)
    for s in Q4State.all_states():
        t.add_row(
            str(s.id), s.binary,
            str(s.C), str(s.R), str(s.E), str(s.P),
            str(s.gray_id), "4.0",
        )
    console.print(t)
