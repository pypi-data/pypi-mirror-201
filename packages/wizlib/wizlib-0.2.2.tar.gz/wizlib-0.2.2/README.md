# WizLib

A collection of Python modules that might be useful across multiple projects

## RLInput

Python supports the GNU readline approach, which enables tab completion, key mappings, and history with the `input()` function. But the documentation is cryptic, and the implementation differs between Linux and MacOS. RLInput makes it easy.

```python
from wizlib.rlinput import rlinput
```

It's just a function, with up to three parameters:

- `intro:str=""` - The intro or prompt, same as in the `input()` function.
- `default:str=""` - If provided, the text will be inserted into the buffer at the start, with the cursor at the end of the buffer. So that becomes the default, that must be overridden by the user if they want different input.
- `options:list=[]` - A list of options for tab completion. This assumes the options are choices for the entire entry; it's not context-dependent within the buffer.

Emacs keys are enabled by default; I'm able to use the arrow keys on my Mac so you should too. I made one change to the keyboard mappings, which is the Ctrl-A, instead of just moving the cursor to the beginning of the line, wipes the entire buffer. So to wipe out the default value and type or tab something new, just hit Ctrl-A.

---

Logo by [Freepik](https://www.freepik.com/?_gl=1*1y9rvc9*test_ga*Mjc1MTIzODYxLjE2ODA3OTczNTg.*test_ga_523JXC6VL7*MTY4MDc5NzM1OC4xLjEuMTY4MDc5NzQxNS4zLjAuMA..*fp_ga*Mjc1MTIzODYxLjE2ODA3OTczNTg.*fp_ga_1ZY8468CQB*MTY4MDc5NzM1OC4xLjEuMTY4MDc5NzQxNS4zLjAuMA..)


