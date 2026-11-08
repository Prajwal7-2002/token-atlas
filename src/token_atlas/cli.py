"""TokenAtlas CLI: Universal Multilingual Tokenizer Benchmark."""

import json
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from token_atlas import __version__
from token_atlas.corpora import SUPPORTED_LANGUAGES
from token_atlas.registry import TokenizerRegistry
from token_atlas.engine import compare_single_text, run_benchmark

app = typer.Typer(
    name="token-atlas",
    help="TokenAtlas: Universal Multilingual Tokenizer Benchmark & Global Inflation Atlas",
    add_completion=False,
)
console = Console()


def version_callback(value: bool):
    if value:
        console.print(f"[bold cyan]TokenAtlas[/bold cyan] version [bold green]{__version__}[/bold green]")
        raise typer.Exit()


@app.callback()
def callback(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", help="Show version and exit", callback=version_callback, is_eager=True
    ),
):
    pass


def main():
    app()


@app.command("list-tokenizers")
def list_tokenizers():
    """List all supported frontier tokenizer architectures and metadata."""
    reg = TokenizerRegistry()
    table = Table(title="[bold cyan]Supported Tokenizers in TokenAtlas[/bold cyan]")
    table.add_column("ID", style="bold green")
    table.add_column("Display Name", style="white")
    table.add_column("Vocab Size", justify="right", style="cyan")
    table.add_column("Context Window", justify="right", style="magenta")
    table.add_column("Backend", style="yellow")

    for spec in reg.list_tokenizers():
        table.add_row(
            spec.id,
            spec.name,
            f"{spec.vocab_size:,}",
            f"{spec.context_window:,} tok",
            spec.backend,
        )
    console.print(table)


@app.command("list-languages")
def list_languages():
    """List all supported language evaluation benchmarks and language families."""
    table = Table(title="[bold cyan]Supported Languages (FLORES-200 Parallel Corpus)[/bold cyan]")
    table.add_column("Code", style="bold green", justify="center")
    table.add_column("Language", style="white")
    table.add_column("Family", style="magenta")
    table.add_column("Script", style="yellow")

    for meta in SUPPORTED_LANGUAGES.values():
        table.add_row(meta.code, meta.name, meta.family, meta.script)
    console.print(table)


@app.command("compare")
def compare_cmd(
    text: str = typer.Option(..., "--text", "-t", help="Text to tokenize across models"),
    tokenizers: str = typer.Option("gpt-4o,gpt-4", "--tokenizers", "-m", help="Comma-separated tokenizer IDs"),
    language: str = typer.Option("en", "--language", "-l", help="Language code (e.g. en, ja, hi, de)"),
):
    """Compare how multiple tokenizers encode a single text string."""
    tids = [t.strip() for t in tokenizers.split(",") if t.strip()]
    comp = compare_single_text(text, tids, language=language)

    console.print(Panel(f"[bold white]{text}[/bold white]", title=f"[bold cyan]Input Text ({comp.language_name})[/bold cyan]"))

    table = Table(title="[bold]Tokenizer Efficiency Comparison[/bold]")
    table.add_column("Tokenizer", style="bold green")
    table.add_column("Tokens", justify="right", style="cyan")
    table.add_column("Bytes", justify="right", style="white")
    table.add_column("Bytes / Token", justify="right", style="magenta")
    table.add_column("First Token Pieces (Sample)", style="dim")

    for res in comp.results:
        pieces_display = " ".join([f"[{p}]" for p in res.token_pieces[:10]])
        table.add_row(
            res.tokenizer_id,
            str(res.token_count),
            str(res.byte_count),
            f"{res.bytes_per_token:.2f}",
            pieces_display,
        )
    console.print(table)


@app.command("bench")
def bench_cmd(
    tokenizers: str = typer.Option("gpt-4o,gpt-4", "--tokenizers", "-m", help="Comma-separated tokenizer IDs"),
    languages: str = typer.Option("en,de,fr,es,ru,ar,hi,kn,zh,ja", "--languages", "-l", help="Comma-separated language codes"),
    samples: int = typer.Option(5, "--samples", "-n", help="Number of parallel sentences to evaluate"),
    json_out: Optional[Path] = typer.Option(None, "--json-out", help="Path to export raw JSON report"),
    md_out: Optional[Path] = typer.Option(None, "--md-out", help="Path to export markdown summary"),
):
    """Run cross-lingual benchmark across parallel sentences and compute inflation indices."""
    tids = [t.strip() for t in tokenizers.split(",") if t.strip()]
    langs = [lang.strip() for lang in languages.split(",") if lang.strip()]

    with console.status("[bold cyan]Running parallel multilingual benchmark...[/bold cyan]"):
        report = run_benchmark(tokenizer_ids=tids, language_codes=langs, sample_limit=samples)

    for bench in report.results:
        table = Table(title=f"[bold cyan]{bench.tokenizer_name} (Vocab: {bench.vocab_size:,})[/bold cyan]")
        table.add_column("Lang", style="bold green", justify="center")
        table.add_column("Language Name", style="white")
        table.add_column("Family", style="dim")
        table.add_column("Tokens", justify="right", style="white")
        table.add_column("Inflation (τ)", justify="right", style="bold yellow")
        table.add_column("Effective Context", justify="right", style="cyan")
        table.add_column("Cost Multiplier", justify="right", style="magenta")
        table.add_column("Bytes/Tok", justify="right", style="dim")

        for code, m in bench.metrics.items():
            tau_style = "bold green" if m.inflation_index <= 1.2 else ("bold yellow" if m.inflation_index <= 2.0 else "bold red")
            table.add_row(
                m.language_code,
                m.language_name,
                m.family,
                f"{m.token_count:,}",
                f"[{tau_style}]{m.inflation_index:.2f}x[/{tau_style}]",
                f"{m.effective_context:,}",
                f"{m.cost_multiplier:.2f}x",
                f"{m.bytes_per_token:.2f}",
            )
        console.print(table)
        console.print()

    if json_out:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        with open(json_out, "w", encoding="utf-8") as f:
            json.dump(report.model_dump(), f, indent=2)
        console.print(f"[bold green]✓ Exported JSON report to {json_out}[/bold green]")

    if md_out:
        md_out.parent.mkdir(parents=True, exist_ok=True)
        with open(md_out, "w", encoding="utf-8") as f:
            f.write(f"# TokenAtlas Multilingual Benchmark Report\n\n")
            f.write(f"- **Evaluated:** {report.timestamp}\n")
            f.write(f"- **Source:** {report.corpora_source}\n")
            f.write(f"- **Sample Sentences:** {samples}\n\n")
            for bench in report.results:
                f.write(f"## {bench.tokenizer_name} (Vocab: {bench.vocab_size:,})\n\n")
                f.write("| Language | Code | Family | Tokens | Inflation Index (τ) | Effective Context | Cost Multiplier | Bytes / Token |\n")
                f.write("| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |\n")
                for m in bench.metrics.values():
                    f.write(f"| {m.language_name} | `{m.language_code}` | {m.family} | {m.token_count:,} | **{m.inflation_index:.2f}x** | {m.effective_context:,} | {m.cost_multiplier:.2f}x | {m.bytes_per_token:.2f} |\n")
                f.write("\n")
        console.print(f"[bold green]✓ Exported Markdown summary to {md_out}[/bold green]")


if __name__ == "__main__":
    app()
