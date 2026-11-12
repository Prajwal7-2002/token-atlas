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
from token_atlas.web import generate_web_dashboard

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
def list_tokenizers(
    category: Optional[str] = typer.Option(
        None, "--category", "-c", help="Filter by category (general, multilingual, code, reasoning, slm)"
    )
):
    """List all supported frontier tokenizer architectures and metadata."""
    reg = TokenizerRegistry()
    title_suffix = f" (Category: {category})" if category else ""
    table = Table(title=f"[bold cyan]Supported Tokenizers in TokenAtlas{title_suffix}[/bold cyan]")
    table.add_column("ID", style="bold green", no_wrap=True)
    table.add_column("Display Name", style="white")
    table.add_column("Category", style="blue", no_wrap=True)
    table.add_column("Vocab Size", justify="right", style="cyan", no_wrap=True)
    table.add_column("Context Window", justify="right", style="magenta", no_wrap=True)
    table.add_column("Backend", style="yellow", no_wrap=True)
    table.add_column("Key Strengths & Compression Profile", style="dim white")

    for spec in reg.list_tokenizers(category=category):
        table.add_row(
            spec.id,
            spec.name,
            spec.category.upper(),
            f"{spec.vocab_size:,}",
            f"{spec.context_window:,} tok",
            spec.backend,
            spec.notes or "—",
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
    text: Optional[str] = typer.Option(None, "--text", "-t", help="Text to tokenize across models"),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="Path to text file to tokenize"),
    tokenizers: str = typer.Option("gpt-4o,gpt-4", "--tokenizers", "-m", help="Comma-separated tokenizer IDs"),
    language: str = typer.Option("en", "--language", "-l", help="Language code (e.g. en, ja, hi, de)"),
):
    """Compare how multiple tokenizers encode a single text string or file."""
    if file is not None:
        if not file.exists():
            console.print(f"[bold red]Error: File not found at {file}[/bold red]")
            raise typer.Exit(1)
        raw_text = file.read_text(encoding="utf-8")
    elif text is not None:
        raw_text = text
    else:
        console.print("[bold red]Error: Either --text or --file must be specified.[/bold red]")
        raise typer.Exit(1)

    tids = [t.strip() for t in tokenizers.split(",") if t.strip()]
    comp = compare_single_text(raw_text, tids, language=language)

    preview = raw_text[:300] + "..." if len(raw_text) > 300 else raw_text
    console.print(Panel(f"[bold white]{preview}[/bold white]", title=f"[bold cyan]Input Text ({comp.language_name})[/bold cyan]"))

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
    languages: str = typer.Option("all", "--languages", "-l", help="Comma-separated language codes or 'all'"),
    samples: int = typer.Option(5, "--samples", "-n", help="Number of parallel sentences to evaluate"),
    custom_corpus: Optional[Path] = typer.Option(None, "--custom-corpus", help="Path to JSON file containing list of parallel sentence dicts"),
    json_out: Optional[Path] = typer.Option(None, "--json-out", help="Path to export raw JSON report"),
    md_out: Optional[Path] = typer.Option(None, "--md-out", help="Path to export markdown summary"),
):
    """Run cross-lingual benchmark across parallel sentences and compute inflation indices."""
    tids = [t.strip() for t in tokenizers.split(",") if t.strip()]
    
    if languages.strip().lower() == "all":
        langs = list(SUPPORTED_LANGUAGES.keys())
    else:
        langs = [lang.strip() for lang in languages.split(",") if lang.strip()]

    corpus_data = None
    source_name = None
    if custom_corpus is not None:
        if not custom_corpus.exists():
            console.print(f"[bold red]Error: Custom corpus file not found at {custom_corpus}[/bold red]")
            raise typer.Exit(1)
        with open(custom_corpus, "r", encoding="utf-8") as f:
            corpus_data = json.load(f)
        source_name = f"Custom Corpus ({custom_corpus.name})"

    with console.status("[bold cyan]Running parallel multilingual benchmark...[/bold cyan]"):
        report = run_benchmark(
            tokenizer_ids=tids,
            language_codes=langs,
            sample_limit=samples,
            custom_corpus=corpus_data,
            corpora_source=source_name,
        )

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


@app.command("export-web")
def export_web_cmd(
    benchmark_json: Path = typer.Option(
        Path("benchmarks/flores200_benchmark.json"),
        "--benchmark-json",
        "-b",
        help="Path to precomputed benchmark JSON report",
    ),
    out_dir: Path = typer.Option(
        Path("docs"),
        "--out-dir",
        "-o",
        help="Output directory for static web dashboard",
    ),
):
    """Generate standalone interactive Web Atlas dashboard for GitHub Pages / HF Space."""
    if not benchmark_json.exists():
        console.print(f"[bold red]Error: Benchmark report not found at {benchmark_json}[/bold red]")
        console.print("Run 'token-atlas bench --languages all --json-out benchmarks/flores200_benchmark.json' first.")
        raise typer.Exit(1)

    with open(benchmark_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    with console.status(f"[bold cyan]Compiling interactive Web Atlas into {out_dir}...[/bold cyan]"):
        out_file = generate_web_dashboard(data, out_dir=out_dir)

    console.print(f"[bold green]✓ Successfully generated Web Atlas dashboard at {out_file}[/bold green]")
    console.print(f"[dim]Deployable directly to GitHub Pages (docs/) or Hugging Face Spaces (static HTML).[/dim]")


@app.command("explain-bytes")
def explain_bytes_cmd(
    text: str = typer.Option(..., "--text", "-t", help="Text to inspect UTF-8 byte breakdown"),
):
    """Diagnose UTF-8 byte layout and explain tokenizer byte-fallback fragmentation."""
    from token_atlas.bpe import explain_fragmentation
    diag = explain_fragmentation(text)

    console.print(Panel(f"[bold white]{text}[/bold white]", title="[bold cyan]UTF-8 Byte Fragmentation Diagnostic[/bold cyan]"))
    console.print(f"Characters: [bold cyan]{diag['character_count']}[/bold cyan] | UTF-8 Bytes: [bold magenta]{diag['utf8_byte_count']}[/bold magenta] | Density: [bold yellow]{diag['bytes_per_char']:.2f} bytes/char[/bold yellow]\n")

    table = Table(title="[bold]Per-Character UTF-8 Byte Breakdown[/bold]")
    table.add_column("Char", style="bold green", justify="center")
    table.add_column("Unicode", style="cyan")
    table.add_column("Bytes", justify="right", style="magenta")
    table.add_column("Raw Hex Bytes", style="dim")

    for item in diag["sample_breakdown"]:
        table.add_row(item["char"], item["unicode"], str(item["byte_count"]), item["raw_hex"])
    console.print(table)


if __name__ == "__main__":
    app()
