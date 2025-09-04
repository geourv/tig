# Jekyll GitBook Template

A ready-to-use template for creating a GitBook-style website using [Jekyll](https://jekyllrb.com/), the [jekyll-gitbook](https://github.com/sighingnow/jekyll-gitbook) theme, and [jekyll-scholar](https://github.com/inukshuk/jekyll-scholar) for managing academic references.

## Table of Contents

- [Features](#features)
- [Setup](#setup)
- [How to Use](#how-to-use)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- **GitBook-style layout:** Clean and responsive design that mimics GitBook.
- **Jekyll Scholar integration:** Seamlessly manage and display academic references.
- **Easy setup:** Simple installation process with clear instructions.
- **Customization:** Easily tweak the design and functionality to suit your needs.
- **Markdown support:** Write your content in Markdown.

## Setup

### Prerequisites

To get started, make sure you have the following installed:

- [Ruby](https://www.ruby-lang.org/en/downloads/) (version 2.5.0 or higher)
- [Bundler](https://bundler.io/)
- [Jekyll](https://jekyllrb.com/)

### Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```
2. **Install the dependencies:**
   ```bash
   bundle install
   ```
4. **Run the Jekyll server:**
   ```bash
   bundle exec jekyll serve
   ```
5. **Visit your site:**
Open your web browser and navigate to `http://localhost:4000`.

# How to Use
## Adding Content

- **Markdown files:** Add your content in the `_posts` directory for blog-style posts or directly into specific folders for chapters or sections.
- **Bibliography:** Manage your references by editing the `references.bib` file located in the root directory. You can then cite them in your markdown files using the `jekyll-scholar` syntax.

## Building the Site

When you are ready to deploy your site, you can build it using:
```bash
bundle exec jekyll build
```
The generated static files will be placed in the `_site` directory, ready to be hosted on GitHub Pages or any other static site hosting platform.
Customizing the Theme

You can customize the theme by modifying the `_config.yml` file and the styles in the `assets/css` directory.

- **Config options:** Change site-wide settings such as title, description, and navigation in `_config.yml`.
- **Layout and styles:** Tweak the layout in _layouts and `_includes`, and update styles in `assets/css/style.css`.

# Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements or new features.

# Basic Markdown Syntax

The content of this book is primarily written in Markdown, a lightweight markup language designed for easy reading and writing. Here are the fundamental elements you can use:

## Headings
Use the hash symbol (`#`) followed by a space to create headings of different levels.  
- One hash (`#`) is for the main title.  
- Two (`##`) for a subtitle.  
- And so on.  

## Bold and Italics
- Use **double asterisks** for bold text.  
- Use *single asterisks* for italics.  

## Lists
- Unordered lists can be created using hyphens (`-`) or asterisks (`*`).  
- Ordered lists use numbers followed by a period (`1.`, `2.`, etc.).  

## Links
Create links with the following syntax:  
```markdown
[Link text](URL)
```

## Images
Insert images using the syntax:  
```markdown
![Alt text](Image_URL)
```

## Tables
Construct tables using vertical bars (`|`) to separate columns and hyphens (`-`) for the separator line.  

For wide tables, wrap the table in a `div` with the class `table-wrapper` to ensure they display correctly on mobile devices.  

---

# Advanced Features

This Jekyll project includes several Markdown extensions to enhance your content's presentation.

## Alert Blocks

You can create styled alert blocks to highlight important information.  
These blocks are written as blockquotes (`>`) followed by a class attribute on a new line.

### Examples

#### Tip block
```markdown
> ##### TIP
>
> This guide was last tested with @napi-rs/canvas^0.1.20, so make sure you have
> this or a similar version after installation.
{: .block-tip }
```

#### Warning block
```markdown
> ##### WARNING
>
> The dataset used in this example is incomplete. Double-check the source before
> using it in production.
{: .block-warning }
```

#### Danger block
```markdown
> ##### DANGER
>
> Removing this directory will permanently delete all your data.
{: .block-danger }
```

### Notes
- The `#####` heading inside the blockquote makes the label (TIP, WARNING, DANGER) stand out.  
- The styling (`.block-tip`, `.block-warning`, `.block-danger`) is handled by the theme’s CSS.  
- You can add any Markdown content inside these blocks: text, links, code, or lists.
## MathJax and LaTeX
This theme supports **MathJax** to render LaTeX and mathematical expressions.  

- Inline expressions: Use a single dollar sign at the beginning and end of the expression, for example: `$x^2 + y^2 = z^2$`.  
- Display equations: For more complex expressions, use double dollar signs on separate lines to create a display block.  

## Footnotes
You can add footnotes to your content to provide additional context or citations.  
Simply include a footnote marker (`[^1]`) in the text and define the note at the end of the file.  

## Syntax Highlighting
To display code blocks cleanly with color, use three backticks (```) to open and close the block.  
Specify the programming language right after the opening backticks for proper highlighting.  

```python
def hello_world():
    print("Hello, world!")
```

## Mermaid Diagrams
This Jekyll theme allows you to use Mermaid diagrams, which let you create charts and graphs from simple text syntax.  
To enable this feature in a chapter, you must add `mermaid: true` to the YAML front matter of the file.  

---

## Bibliography Management

This template includes the **Jekyll Scholar** plugin, a powerful tool for managing bibliographies and citations.  
This makes it an excellent choice for academic or technical documentation where you need to reference external sources.

To use this feature, follow these steps:

1. **Installation**: Add `gem 'jekyll-scholar'` to your `Gemfile` and run `bundle install`.  
2. **Configuration**: In `_config.yml`, add a `scholar:` block to specify your citation style, locale, and the path to your bibliography file.  
3. **Create a `.bib` file**: Add your references in BibTeX format to a `.bib` file (e.g., `references.bib`) within the `_bibliography` folder.  
4. **Citing**: Cite references directly in your posts using the `{% cite %}` tag with the BibTeX key.  
5. **Displaying the bibliography**: Use the `{% bibliography %}` tag to display a complete list of your references at the end of a page or post.  

# License

This project is licensed under the MIT License. See the LICENSE file for more details.

# Acknowledgements

This template is built with:

- [jekyll-gitbook](https://github.com/sighingnow/jekyll-gitbook) by [Sighingnow](https://github.com/sighingnow)
- [jekyll-scholar](https://github.com/inukshuk/jekyll-scholar) by [Inukshuk](https://github.com/inukshuk)

Check out their projects for more detailed documentation and updates.


