# Expression Differentiator using Abstract Syntax Trees

## Description
This Python implementation demonstrates symbolic differentiation of mathematical expressions using Abstract Syntax Trees (AST).

## Features
- ✅ Parses mathematical expressions with operators (`+`, `-`, `*`, `/`, `^`)
- ✅ Supports trigonometric, inverse trigonometric, logarithmic, and root functions
- ✅ Converts infix → RPN → AST representation
- ✅ Performs symbolic differentiation
- ✅ Outputs differentiated expressions in infix notation

## Supported Functions

| Function | Derivative |
|----------|------------|
| `sin(x)` | `cos(x)` |
| `cos(x)` | `-sin(x)` |
| `tan(x)` | `1/cos²(x)` |
| `ctg(x)` | `-1/sin²(x)` |
| `arcsin(x)` | `1/√(1-x²)` |
| `arccos(x)` | `-1/√(1-x²)` |
| `arctg(x)` | `1/(1+x²)` |
| `arcctg(x)` | `-1/(1+x²)` |
| `ln(x)` | `1/x` |
| `√(x)` | `1/(2√x)` |

## Usage
1. Edit the `exp` variable in `main()`
2. Run the script:
```bash
python main.py
```
## Example:
```python
exp = "x^2 + 3*sin(x)"
# Output: (2 * x) + (3 * cos(x))