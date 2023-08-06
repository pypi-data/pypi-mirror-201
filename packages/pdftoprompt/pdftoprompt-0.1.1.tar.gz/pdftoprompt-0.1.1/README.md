# PDFtoPrompt

[![PyPI version](https://badge.fury.io/py/pdftoprompt.svg)](https://badge.fury.io/py/pdftoprompt)

Existing libraries for using GPT-4 to extract information from a PDF fil typically combine GPT-4 with word searching, indexing, and segmentation. Those strategies work reasonably, but they have one significant limitation: they deprive the LLM of "big picture" context.

PDFtoPrompt takes a different strategy. Inspired by Twitter user [@gfodor](https://twitter.com/gfodor)'s experiments with [text compression](https://twitter.com/gfodor/status/1643415357615640577), it uses GPT-4 to compress or distill a PDF file's entire informational content to below the length limit of a single ChatGPT prompt. 

It achieves this by first calculating what compression factor is needed to get the text to the right length, then segmenting the PDF file and asking GPT-4 to compress each segment, and finally stitching the compressed segments back together. You should then be able to fit the full compressed text into a single ChatGPT prompt, with some room left over to ask a question.

The process is, as @gfodor notes, pretty "lossy," especially for longer texts. This tool may be best used in combination with others built on other strategies.

## Installation

1. Install with pip:

```bash
pip install pdftoprompt
```

## Usage

### Setting your API Key

Make sure to first set your GPT-4-approved OpenAI API key with the set_openai_api_key function:


```python
from pdftoprompt import set_openai_api_key

set_openai_api_key()
```

This function either takes your API key as a string argument or looks in the .env file in the current working directory to see if you have an OPENAI_API_KEY variable stored there. I recommend saving your API key in the .env file for your project so you can share your code without worrying about key security. If you're uploading code to GitHub, make sure to add .env to .gitignore.

### Compressing a PDF to an LLM Prompt

Next, import the `compress_pdf` function from the `pdftoprompt` library, and call it with the PDF url or file path:


```python
from pdftoprompt import compress_pdf

file_path = "https://arxiv.org/pdf/2203.06566.pdf"

compressed_text = compress_pdf(file_path)
print(compressed_text)
```


The above code distills an academic paper titled ["PromptChainer: Chaining Large Language Model Prompts through Visual Programming"](https://arxiv.org/pdf/2203.06566.pdf) down to the following GPT-interpretable prompt:

"PromptChainer: Chaining LLM Prompts through Visual Programming\nAuthors: Tongshuang Wu, Ellen Jiang, Aaron Donsbach, Jeff Gray, Alejandra Molina, Michael Terry, Carrie J. Cai\n\nABSTRACT:\nLLMs enable rapid prototyping of ML functionalities, but complex tasks need chaining multiple LLM runs. PromptChainer is an interactive interface for visually programming chains. Case studies with designers and developers show it supports building prototypes for various applications. Open questions involve scaling chains for more complex tasks and supporting low-fi chain prototyping.\n\n1 INTRODUCTION:\nLLMs like GPT-3 and Jurassic-1 allow easy customization for new tasks using natural language prompts. However, complex tasks may require chaining multiple LLM runs. PromptChainer aims to support users in authoring their own LLM chains.\n\n3 PROMPTCHAINER: INTERFACE REQUIREMENT ANALYSIS & DESIGN:\nChallenges in authoring chains include:\nC.1: Versatility of LLMs and need for data transformations\nC.2: Instability of LLM function signatures\nC.3: Likelihood of cascading errors\n\nPromptChainer addresses these challenges with a Chain View for authoring chain structure, a Node View for implementing individual nodes, and debugging features.\n\n4 CASE STUDIES: AUTHORS BUILDING LLM CHAINS:\nQualitative analysis of case studies with designers and developers reveals patterns in chain building and debugging. Open challenges include scaling chains for tasks with high interdependency or logical complexity and finding a sweet spot for prompting to quickly prototype multiple alternative chains.(Figure 1B) for single step (node) authoring and chain debugging support. Chain View: visual panel for building/viewing chains (Figure 1A). Nodes represent chain steps, edges denote connections/input-output flow. Node visualization (Figure 4): named inputs (𝑎2) and outputs (𝑎3) to connect nodes. Inspired by node-edge-based visual programming platforms2, we provide node previews for chaining transparency, including status icon (errors) (Figure 4𝑎1) and data views (𝑎3and𝑎4). Node Types (Figure 3): LLM nodes (Generic, Classifier), helper nodes (data transformation, evaluation, custom JavaScript), communication nodes (external API calls). Example gallery for versatility, prompting patterns.\n\nNode View: inspect, implement, test individual nodes (Figure 1B). PromptChainer parses input names based on LLM prompt/node type, updates global chain with local edits (addressing C.2). Interactive debugging: unit test nodes (Figure 4𝑐1), end-to-end assessment/logging (Figure 4 𝑐2), breakpoint debugging/output editing (Figure 4𝑐3).\n\nUser feedback sessions (preliminary study): 4 participants (3 designers, 1 developer) with prior non-chained prompt experience. Study focused on chaining prompts, interface tutorial, and task completion sessions. Underlying LLM: LaMDA [16] (137 billion parameters, comparable to GPT-3). Study results: users built diverse chains (branching logic, iterating content, extensible prototypes) using PromptChainer, supporting various construction strategies and multi-level debugging. Remaining challenges: coherence between interdependent sub-tasks, tracking user contributions, and supporting chain debugging.Chains with complex logic and interdependent parallel tasks can decrease coherence. P4\'s story writing chain generated a paragraph for each outline point, resulting in a less coherent essay. A similar challenge was faced by a pilot study user, prompting future investigation into methods considering inter-dependency.\n\nComplex decomposition in chains can be overwhelming to track, as seen in P1\'s music chatbot chain. Enhancing tracing capabilities and execution visualizations is a potential solution.\n\nPre-creating LLM prompts for sub-tasks might lead to users feeling invested in their chain decomposition, limiting exploration of other structures. Encouraging low-fi prototyping of multiple chains and supporting "half-baked" chain construction can improve outcomes.\n\nTime constraints and task decomposition strategies for larger, complex tasks should be explored. PromptChainer can encourage further node decomposition if extensive prompting efforts are unsuccessful."

Note that when we ask GPT to compress the text, we specifically instruct it that the text doesn't have to be human-readable. The goal here isn't to get a shortened version that works for humans. It's to get a shortened version that works as a Large Language Model prompt.

### OCR

In theory, you should be able to use OCR by setting the `compress_pdf` function's `use_ocr` argument to True, but that functionality requires that you install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and add it to your system path, and I can't vouch for this functionality because I haven't tested it yet.

## Contributing

If you'd like to contribute to this library, please submit a pull request on GitHub.

## License

This library is released under the [MIT License](https://opensource.org/licenses/MIT).
