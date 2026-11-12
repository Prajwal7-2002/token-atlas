"""Multi-Domain Tokenization Benchmark: Code, Indentation, Tools, and Math.

Quantifies the hidden token taxes beyond prose:
1. Indentation Tax (4-space vs 2-space vs tabs vs minified)
2. Code Syntax Tax (Python vs TypeScript vs Rust vs Go vs SQL)
3. Agent Tool-Calling Schema Tax (Verbose OpenAPI/JSON vs Compact JSON)
4. Mathematical Representation Tax (LaTeX vs Unicode vs Pure Code)
"""

from typing import Any, Optional
from pydantic import BaseModel, Field

from token_atlas.registry import TokenizerRegistry
from token_atlas.metrics import calculate_bytes_per_token


class DomainSample(BaseModel):
    """A single evaluation text snippet within a specific domain."""
    id: str
    title: str
    domain: str  # "code", "indentation", "tools", "math"
    variant: str  # e.g., "python", "rust", "spaces_4", "minified"
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)


# -----------------------------------------------------------------------------
# 1. PARALLEL CODE CORPUS (Canonical Algorithms across 5 Languages)
# -----------------------------------------------------------------------------

QUICKSORT_PYTHON = """def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
"""

QUICKSORT_TYPESCRIPT = """function quickSort(arr: number[]): number[] {
    if (arr.length <= 1) return arr;
    const pivot = arr[Math.floor(arr.length / 2)];
    const left = arr.filter(x => x < pivot);
    const middle = arr.filter(x => x === pivot);
    const right = arr.filter(x => x > pivot);
    return [...quickSort(left), ...middle, ...quickSort(right)];
}
"""

QUICKSORT_RUST = """pub fn quicksort<T: Ord + Clone>(slice: &[T]) -> Vec<T> {
    if slice.len() <= 1 {
        return slice.to_vec();
    }
    let pivot = &slice[slice.len() / 2];
    let left: Vec<T> = slice.iter().filter(|&x| x < pivot).cloned().collect();
    let middle: Vec<T> = slice.iter().filter(|&x| x == pivot).cloned().collect();
    let right: Vec<T> = slice.iter().filter(|&x| x > pivot).cloned().collect();
    [quicksort(&left), middle, quicksort(&right)].concat()
}
"""

QUICKSORT_GO = """package main

func quickSort(arr []int) []int {
    if len(arr) <= 1 {
        return arr
    }
    pivot := arr[len(arr)/2]
    var left, middle, right []int
    for _, x := range arr {
        switch {
        case x < pivot:
            left = append(left, x)
        case x == pivot:
            middle = append(middle, x)
        case x > pivot:
            right = append(right, x)
        }
    }
    result := append(quickSort(left), middle...)
    return append(result, quickSort(right)...)
}
"""

QUICKSORT_SQL = """WITH RECURSIVE sort_cte AS (
    SELECT id, value, ROW_NUMBER() OVER (ORDER BY value ASC) as rank
    FROM raw_elements
)
SELECT id, value
FROM sort_cte
ORDER BY rank ASC;
"""

# -----------------------------------------------------------------------------
# 2. INDENTATION TAX CORPUS (Nested Control Flow across Spacing Schemes)
# -----------------------------------------------------------------------------

INDENT_SPACES_4 = """class NetworkTrafficAnalyzer:
    def process_packet(self, packet):
        if packet.is_valid():
            payload = packet.get_payload()
            if payload.has_header():
                for header in payload.headers:
                    if header.is_priority():
                        self.queue_urgent(header)
                    else:
                        self.queue_standard(header)
            else:
                self.log_corrupt(packet)
        else:
            self.drop(packet)
"""

INDENT_SPACES_2 = """class NetworkTrafficAnalyzer:
  def process_packet(self, packet):
    if packet.is_valid():
      payload = packet.get_payload()
      if payload.has_header():
        for header in payload.headers:
          if header.is_priority():
            self.queue_urgent(header)
          else:
            self.queue_standard(header)
      else:
        self.log_corrupt(packet)
    else:
      self.drop(packet)
"""

INDENT_TABS = """class NetworkTrafficAnalyzer:
\tdef process_packet(self, packet):
\t\tif packet.is_valid():
\t\t\tpayload = packet.get_payload()
\t\t\tif payload.has_header():
\t\t\t\tfor header in payload.headers:
\t\t\t\t\tif header.is_priority():
\t\t\t\t\t\tself.queue_urgent(header)
\t\t\t\t\telse:
\t\t\t\t\t\tself.queue_standard(header)
\t\t\t\telse:
\t\t\t\t\tself.log_corrupt(packet)
\t\telse:
\t\tself.drop(packet)
"""

INDENT_MINIFIED = """class NetworkTrafficAnalyzer:\n def process_packet(self,p):\n  if p.is_valid():\n   pl=p.get_payload()\n   if pl.has_header():\n    for h in pl.headers:\n     self.queue_urgent(h) if h.is_priority() else self.queue_standard(h)\n   else:self.log_corrupt(p)\n  else:self.drop(p)"""

# -----------------------------------------------------------------------------
# 3. AGENT TOOL-CALLING & JSON SCHEMA CORPUS
# -----------------------------------------------------------------------------

TOOL_SCHEMA_VERBOSE = """{
  "name": "query_database_records",
  "description": "Execute a structured SQL query against the customer analytics database to retrieve matching records.",
  "parameters": {
    "type": "object",
    "properties": {
      "table_name": {
        "type": "string",
        "description": "The exact name of the table to query, e.g., 'orders', 'users', 'invoices'."
      },
      "filters": {
        "type": "array",
        "description": "List of filtering conditions applied to rows.",
        "items": {
          "type": "object",
          "properties": {
            "column": { "type": "string" },
            "operator": { "type": "string", "enum": ["eq", "gt", "lt", "like", "in"] },
            "value": { "type": "string" }
          },
          "required": ["column", "operator", "value"]
        }
      },
      "limit": {
        "type": "integer",
        "description": "Maximum number of records to return (1-1000).",
        "default": 100
      }
    },
    "required": ["table_name", "filters"]
  }
}"""

TOOL_SCHEMA_COMPACT = """{"name":"query_database_records","parameters":{"type":"object","properties":{"table_name":{"type":"string"},"filters":{"type":"array","items":{"type":"object","properties":{"column":{"type":"string"},"operator":{"type":"string","enum":["eq","gt","lt","like","in"]},"value":{"type":"string"}},"required":["column","operator","value"]}},"limit":{"type":"integer","default":100}},"required":["table_name","filters"]}}"""

TOOL_CALL_ARGS_VERBOSE = """{
  "table_name": "customer_transactions",
  "filters": [
    {
      "column": "status",
      "operator": "eq",
      "value": "completed"
    },
    {
      "column": "amount_usd",
      "operator": "gt",
      "value": "250.00"
    }
  ],
  "limit": 50
}"""

TOOL_CALL_ARGS_COMPACT = """{"table_name":"customer_transactions","filters":[{"column":"status","operator":"eq","value":"completed"},{"column":"amount_usd","operator":"gt","value":"250.00"}],"limit":50}"""

# -----------------------------------------------------------------------------
# 4. MATHEMATICS & FORMULA CORPUS
# -----------------------------------------------------------------------------

ATTENTION_LATEX = r"""\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V"""

ATTENTION_UNICODE = """Attention(Q, K, V) = softmax((Q × Kᵀ) / √dₖ) × V"""

ATTENTION_CODE = """def attention(q, k, v, d_k):
    scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(d_k)
    weights = torch.softmax(scores, dim=-1)
    return torch.matmul(weights, v)
"""

# Corpus registry mapping
DOMAIN_SAMPLES: list[DomainSample] = [
    # Code
    DomainSample(id="code_python", title="QuickSort (Python)", domain="code", variant="python", content=QUICKSORT_PYTHON),
    DomainSample(id="code_typescript", title="QuickSort (TypeScript)", domain="code", variant="typescript", content=QUICKSORT_TYPESCRIPT),
    DomainSample(id="code_rust", title="QuickSort (Rust)", domain="code", variant="rust", content=QUICKSORT_RUST),
    DomainSample(id="code_go", title="QuickSort (Go)", domain="code", variant="go", content=QUICKSORT_GO),
    DomainSample(id="code_sql", title="QuickSort (SQL Recursive)", domain="code", variant="sql", content=QUICKSORT_SQL),
    # Indentation
    DomainSample(id="indent_spaces4", title="4-Space Indentation", domain="indentation", variant="spaces_4", content=INDENT_SPACES_4),
    DomainSample(id="indent_spaces2", title="2-Space Indentation", domain="indentation", variant="spaces_2", content=INDENT_SPACES_2),
    DomainSample(id="indent_tabs", title="Tab Indentation", domain="indentation", variant="tabs", content=INDENT_TABS),
    DomainSample(id="indent_minified", title="Minified / Zero Spacing", domain="indentation", variant="minified", content=INDENT_MINIFIED),
    # Tools
    DomainSample(id="tool_schema_verbose", title="Verbose Tool Schema (JSON)", domain="tools", variant="verbose_schema", content=TOOL_SCHEMA_VERBOSE),
    DomainSample(id="tool_schema_compact", title="Compact Tool Schema (JSON)", domain="tools", variant="compact_schema", content=TOOL_SCHEMA_COMPACT),
    DomainSample(id="tool_call_verbose", title="Verbose Tool Call Args", domain="tools", variant="verbose_args", content=TOOL_CALL_ARGS_VERBOSE),
    DomainSample(id="tool_call_compact", title="Compact Tool Call Args", domain="tools", variant="compact_args", content=TOOL_CALL_ARGS_COMPACT),
    # Math
    DomainSample(id="math_latex", title="Attention Equation (LaTeX)", domain="math", variant="latex", content=ATTENTION_LATEX),
    DomainSample(id="math_unicode", title="Attention Equation (Unicode)", domain="math", variant="unicode", content=ATTENTION_UNICODE),
    DomainSample(id="math_code", title="Attention Equation (PyTorch Code)", domain="math", variant="code", content=ATTENTION_CODE),
]


class DomainEvaluationRow(BaseModel):
    """Evaluation result of a sample under a single tokenizer."""
    sample_id: str
    sample_title: str
    domain: str
    variant: str
    tokenizer_id: str
    token_count: int
    char_count: int
    byte_count: int
    bytes_per_token: float
    relative_inflation: float = Field(1.0, description="Ratio vs baseline within the domain")


class DomainBenchmarkReport(BaseModel):
    """Aggregated benchmark report across one or more evaluation domains."""
    domain: str
    tokenizers: list[str]
    rows: list[DomainEvaluationRow]
    summary_metrics: dict[str, Any] = Field(default_factory=dict)


def evaluate_domain(
    domain: str,
    tokenizer_ids: list[str],
    registry: Optional[TokenizerRegistry] = None,
) -> DomainBenchmarkReport:
    """Evaluate a specific domain ('code', 'indentation', 'tools', 'math', or 'all') across tokenizers."""
    reg = registry or TokenizerRegistry()
    target_samples = [s for s in DOMAIN_SAMPLES if domain == "all" or s.domain == domain]
    if not target_samples:
        valid = sorted(list({s.domain for s in DOMAIN_SAMPLES}))
        raise ValueError(f"Unknown domain '{domain}'. Valid options: {valid} or 'all'")

    rows: list[DomainEvaluationRow] = []

    for sample in target_samples:
        baseline_tokens: Optional[int] = None
        for tok_id in tokenizer_ids:
            res = reg.tokenize(tok_id, sample.content, language="en")
            if baseline_tokens is None:
                baseline_tokens = max(1, res.token_count)
            rel_inf = res.token_count / baseline_tokens

            rows.append(
                DomainEvaluationRow(
                    sample_id=sample.id,
                    sample_title=sample.title,
                    domain=sample.domain,
                    variant=sample.variant,
                    tokenizer_id=tok_id,
                    token_count=res.token_count,
                    char_count=res.char_count,
                    byte_count=res.byte_count,
                    bytes_per_token=res.bytes_per_token,
                    relative_inflation=round(rel_inf, 3),
                )
            )

    # Compute domain summary metrics
    summary: dict[str, Any] = {}
    if domain in ("indentation", "all"):
        # Indentation tax: 4 spaces vs minified
        indent_tax = {}
        for tok_id in tokenizer_ids:
            sp4 = next((r.token_count for r in rows if r.tokenizer_id == tok_id and r.variant == "spaces_4"), None)
            minf = next((r.token_count for r in rows if r.tokenizer_id == tok_id and r.variant == "minified"), None)
            if sp4 and minf:
                indent_tax[tok_id] = round(sp4 / max(1, minf), 2)
        summary["indentation_tax_ratio"] = indent_tax

    if domain in ("tools", "all"):
        # Tool-calling whitespace penalty
        tool_tax = {}
        for tok_id in tokenizer_ids:
            v_schema = next((r.token_count for r in rows if r.tokenizer_id == tok_id and r.variant == "verbose_schema"), None)
            c_schema = next((r.token_count for r in rows if r.tokenizer_id == tok_id and r.variant == "compact_schema"), None)
            if v_schema and c_schema:
                tool_tax[tok_id] = round(v_schema / max(1, c_schema), 2)
        summary["tool_schema_whitespace_tax"] = tool_tax

    return DomainBenchmarkReport(
        domain=domain,
        tokenizers=tokenizer_ids,
        rows=rows,
        summary_metrics=summary,
    )

