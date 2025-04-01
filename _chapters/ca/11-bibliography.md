---
lang: ca
permalink: /:title/ca/
title: 11. Adding bibliographies
author: "Benito Zaragozí"
date: 2024-09-02
category: Jekyll
weight: 11
layout: chapter
---

One of the powerful features of Jekyll is its ability to manage bibliographies and citations directly within your Markdown content, thanks to the Jekyll Scholar plugin. This makes it an excellent choice for academic writing, technical documentation, or any project where you need to reference external sources. In this post, we'll explore how to leverage Jekyll Scholar within your GitBook template to manage bibliographies effectively.

## Setting Up Jekyll Scholar

Before you can start using Jekyll Scholar, you'll need to make sure it's installed and configured in your Jekyll project. Here's how you can get started:

1.  **Install Jekyll Scholar:** Open your `Gemfile` and add the following line:
    
    `gem 'jekyll-scholar'`
    
    Then run `bundle install` to install the gem.
    
2.  **Configure Jekyll Scholar:** In your `_config.yml` file, add a configuration block for Jekyll Scholar. Here’s an example:
    
    `scholar:   style: apa   locale: en   sort_by: year   order: descending   source: _bibliography   bibliography: references.bib`
    
    *   `style`: Specifies the citation style (e.g., APA, MLA, Chicago).
    *   `bibliography`: Points to the BibTeX file where your references are stored.

## Adding Bibliography Files

To start managing your references, you need a `.bib` file containing your bibliography entries:

1.  **Create a `_bibliography` Folder:** Create a folder named `_bibliography` in the root directory of your Jekyll project.
    
    `mkdir _bibliography`
    
2.  **Add a BibTeX File:** Inside the `_bibliography` folder, create a file named `references.bib` (or any name specified in your `_config.yml`). This file will contain all your references in BibTeX format. Here’s an example of what an entry might look like:
    
    `@article{doe2021,   author = {John Doe},   title = {An Interesting Article},   journal = {Journal of Interesting Studies},   year = {2021},   volume = {42},   number = {7},   pages = {123-456},   month = jul,   note = {A special note},   url = {http://example.com/article} }`
    

## Citing References in Your Posts

With your references added, you can now cite them directly in your posts. To do this, use the `cite` tag provided by Jekyll Scholar.

For example, if you want to cite the article by John Doe from the BibTeX file, you would use:

`As discussed by Doe in his study {% cite doe2021 %}, the results were fascinating.`

This will automatically generate a citation according to the style you’ve specified in `_config.yml`.

## Displaying a Bibliography

You can also display a list of all your references at the end of a post or on a dedicated bibliography page. To do this, simply use the `bibliography` tag:

`# References  {% bibliography %}`

This tag will render a full list of all references included in your BibTeX file, formatted according to the citation style you specified.

## Advanced Features

Jekyll Scholar offers a variety of advanced features:

*   **Customizing Bibliographies:** You can display only specific references by adding a query to the `bibliography` tag, like so:
    
    `{% bibliography --query @article %}`
    
    This would display only items categorized as `@article` in your BibTeX file.
    
*   **Linking to PDFs:** If you have PDFs of your references, you can link them directly in your BibTeX file using the `file` field and the Jekyll Scholar `repository` configuration.
    
*   **Sorting and Filtering:** You can sort and filter references based on different criteria, such as author, year, or type.
    

## Conclusion

Using Jekyll Scholar in your GitBook template brings powerful citation management right into your documentation workflow. Whether you’re writing an academic paper, a technical manual, or a simple guide, this tool helps you maintain a professional, well-organized bibliography with minimal effort. By following the steps outlined in this post, you can easily set up and use Jekyll Scholar to manage your references, ensuring that your work is properly cited and accessible.

Happy writing!

# Recommended readings

{% bibliography %}
