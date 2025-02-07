---
title: 1. Why Jekyll with GitBook
author: Tao He
date: 2019-04-27
category: Jekyll
weight: 1
layout: chapter
video: "https://www.youtube.com/watch?v=abc123"
---
GitBook is an amazing frontend style to present and organize contents (such as book chapters
and blogs) on Web. The typical to deploy GitBook at [Github Pages][1]
is building HTML files locally and then push to Github repository, usually to the `gh-pages`
branch. However, it's quite annoying to repeat such workload and make it hard for people do
version control via git for when there are generated HTML files to be staged in and out.

This theme takes style definition out of generated GitBook site and provided the template
for Jekyll to rendering markdown documents to HTML, thus the whole site can be deployed
to [Github Pages][1] without generating and uploading HTML bundle every time when there are
changes to the original repository.

[1]: https://pages.github.com

This Jekyll GitBook template is designed to be a powerful and flexible solution for creating beautiful and easy-to-navigate documentation, manuals, or even personal books. Whether you're a developer, a technical writer, or anyone needing to compile and present information in a structured format, this template offers a user-friendly way to do so.

#### Why Use This Jekyll Template?

1.  **Ease of Use:**
    
    *   With Jekyll’s static site generator at its core, this template allows you to focus on writing content in Markdown, while the template handles the organization and styling. You don't need to worry about complex setup or design details—just write and publish.
2.  **GitBook Style Layout:**
    
    *   Inspired by the popular GitBook platform, this template provides a clean and professional layout. It includes an automatic table of contents, sidebar navigation, and customizable themes, ensuring your content is accessible and easy to browse.
3.  **Customizable and Extensible:**
    
    *   Built with flexibility in mind, this template allows you to easily customize layouts, colors, and components to match your branding or personal style. Moreover, it integrates seamlessly with Jekyll plugins, including Jekyll Scholar for citations and bibliographies, making it ideal for academic projects.
4.  **Perfect for Documentation:**
    
    *   Whether you're documenting software, writing a user manual, or creating a knowledge base, this template is equipped to handle it all. The structured format helps you organize content into sections and chapters, making it easier for users to find the information they need.
5.  **Static Site Benefits:**
    
    *   As a Jekyll-based template, your site will be fast, secure, and easy to host. Static sites have fewer vulnerabilities compared to dynamic sites, and they can be hosted on a wide range of platforms, including GitHub Pages, for free.

#### Purpose of This Template

The primary goal of this template is to provide a solid foundation for creating structured, readable, and professional-looking documentation or books. It serves as a starting point that you can quickly adapt to suit your specific needs.

In addition to providing a clean and organized structure for your content, this Jekyll template is designed with advanced features to enhance your documentation or book project. One of the key purposes of this template is to seamlessly integrate bibliography management, allowing you to easily cite sources and compile comprehensive reference lists using **Jekyll Scholar**. Furthermore, it supports PDF compilation, enabling you to generate **print-ready versions** of your content for offline distribution or archival purposes. These features, along with others such as custom layouts and flexible navigation, make this template a robust tool for creating professional, well-organized publications.

This manual will guide you through the process of setting up your project with this template, customizing it to your liking, and understanding the features available to you. By the end of this manual, you’ll be equipped to create and maintain your own beautifully crafted book or documentation site with ease.

* * *

By following the steps outlined in this manual, you'll be able to leverage the full potential of the Jekyll GitBook template, making it easier than ever to create, manage, and share your content with the world.


# Recommended readings

{% bibliography %}
