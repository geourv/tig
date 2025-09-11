# frozen_string_literal: true
# Figures plugin (conservative, robust)
# - Fase 1 (Generator): convierte imágenes Markdown ![alt](URL "title"){...} en <figure>.
#     * Mantiene Liquid en el caption (en el "title"), así jekyll-scholar procesa {% cite %}.
#     * Convierte [texto](url "título") a <a>…</a> dentro del caption (porque Markdown no corre dentro de HTML crudo).
#     * El ALT no lleva Liquid (se purga) para no romper el atributo.
# - Fase 2 (post_render, HTML final): envuelve <p><img ...></p> en <figure> con caption a partir de title→alt.
#     * NO consume párrafos siguientes (evita “absorber” texto).
#     * Desescapa entidades del caption (por si vino HTML de scholar dentro de alt/title).
#
# Requisitos:
# - No usar `safe: true` en _config.yml (o no correrán los plugins).
# - Usar `jekyll` “normal” (no la gem `github-pages`) si compilas fuera de Pages.
# - Conversor: kramdown (por defecto) o pandoc; ambos respetan "title" en la imagen.

require "cgi"

module Jekyll
  module ImageCaptionTools
    module_function

    # ------------ helpers de idioma/etiquetas ------------
    def detect_lang_code(doc)
      rel = doc.relative_path.to_s.tr("\\", "/")
      rel.split("/")[1]
    end

    def figure_label_for(site, lang_code)
      i18n = site.data["i18n"] || {}
      (i18n.dig(lang_code, "figure") || "Figure").to_s
    end

    # ------------ Fase 1: parser robusto de Markdown ------------
    def transform_markdown_images(text, lang, label)
      out = +""
      s = text.to_s
      i = 0
      n = 0

      while i < s.length
        if s[i] == '!' && i + 1 < s.length && s[i + 1] == '['
          parsed = parse_markdown_image(s, i)
          if parsed
            alt, url_and_title, attrs_raw, j = parsed.values_at(:alt, :url_and_title, :attrs, :end_idx)

            # opt-out explícito
            if attrs_raw && attrs_raw.match?(/(\.no-figure|data-no-figure\s*=\s*["'”“’]true["'”“’])/)
              out << s[i...j]
            else
              url, title = split_url_and_title(url_and_title)
              caption_raw  = (title && !title.empty?) ? title : alt
              alt_for_attr = strip_liquid(alt)

              n += 1
              fig_id       = "fig-#{lang}-#{n}"
              attrs_html   = kramdown_attrs_to_html(attrs_raw)
              caption_html = render_inline_links(caption_raw) # permite [texto](url)

              out << "\n\n"
              out << %Q{
<figure id="#{fig_id}" class="md-figure">
  <div class="md-figure-inner">
    <img src="#{url.strip}" alt="#{h(alt_for_attr)}" #{attrs_html}>
  </div>
  #{ caption_html.strip.empty? ? "" : %Q{<figcaption class="md-figcaption"><span class="figlabel">#{label} #{n}.</span> #{caption_html}</figcaption>} }
</figure>
}.strip
              out << "\n\n"
            end
            i = j
            next
          end
        end
        out << s[i]
        i += 1
      end

      out
    end

    # Parse ![ALT](URL "title"){ attrs } desde posición i0 (soporta [] anidados en ALT).
    def parse_markdown_image(s, i0)
      i = i0
      return nil unless s[i] == '!' && s[i + 1] == '['

      i += 2
      alt, i = read_balanced(s, i, '[', ']')
      return nil unless alt && i < s.length && s[i] == ']'

      i += 1
      return nil unless i < s.length && s[i] == '('
      i += 1
      url_and_title, i = read_until_closing_paren(s, i)
      return nil unless url_and_title && i < s.length && s[i] == ')'
      i += 1

      attrs_raw = nil
      i = skip_spaces(s, i)
      if i < s.length && s[i] == '{'
        # accepts Kramdown "{: … }" and Pandoc "{ … }"
        j = i + 1
        j += 1 while j < s.length && s[j] != '}'
        return nil if j >= s.length
        attrs_raw = s[i..j]   # include the braces
        i = j + 1
      end


      { alt: alt, url_and_title: url_and_title, attrs: attrs_raw, end_idx: i }
    end

    def read_balanced(s, i, open_ch, close_ch)
      depth = 1
      start = i
      while i < s.length
        ch = s[i]
        if ch == '\\'; i += 2; next
        elsif ch == open_ch; depth += 1
        elsif ch == close_ch
          depth -= 1
          return [s[start...i], i + 1] if depth == 0
        end
        i += 1
      end
      [nil, i]
    end

    def read_until_closing_paren(s, i)
      depth = 1
      start = i
      while i < s.length
        ch = s[i]
        if ch == '\\'; i += 2; next
        elsif ch == '('; depth += 1
        elsif ch == ')'
          depth -= 1
          return [s[start...i], i] if depth == 0
        end
        i += 1
      end
      [nil, i]
    end

    def skip_spaces(s, i); i += 1 while i < s.length && s[i] =~ /\s/; i end

    # separa URL y "title" final (acepta comillas rectas o curvas)
    def split_url_and_title(str)
      return [str, nil] if str.nil? || str.empty?
      if str =~ /\s*([\"“”'’])([^\"”’']*)\1\s*\z/
        title = $2
        url   = str.sub(/\s*([\"“”'’])([^\"”’']*)\1\s*\z/, "").strip
        [url, title]
      else
        [str, nil]
      end
    end

    # convierte [text](url "title") a <a>; no toca Liquid
    def render_inline_links(str)
      return "" if str.nil? || str.empty?
      str.gsub(/\[([^\]]+)\]\((\S+?)(?:\s+"([^"]*)")?\)/) do
        text, url, title = $1, $2, $3
        if title && !title.empty?
          %Q{<a href="#{h(url)}" title="#{h(title)}">#{text}</a>}
        else
          %Q{<a href="#{h(url)}">#{text}</a>}
        end
      end
    end

    # ------------ Fase 2: fallback HTML conservador ------------
    # Envuelve SOLO <p><img ...></p>. Caption desde title→alt. No toca párrafos siguientes.
    def wrap_html_imgs_in_output(html, lang, label)
      return html unless html.include?("<img")

      # continuar numeración tras figuras ya creadas en fase 1
      n = 0
      html.scan(/<figure\b/i) { n += 1 }

      html.gsub(%r{<p>\s*(<img\b[^>]*>)\s*</p>}mi) do
        img_tag = $1
        # opt-out
        next $& if img_tag =~ /\bdata-no-figure\s*=\s*["']true["']/i

        # caption: title si existe; si no, alt
        cap = extract_attr(img_tag, "title").to_s
        cap = extract_attr(img_tag, "alt").to_s if cap.empty?

        # 1) desescapa entidades por si viniera HTML de scholar en alt/title
        cap_html = CGI.unescapeHTML(cap.to_s)
        # 2) permite enlaces simples [texto](url) dentro del caption
        cap_html = render_inline_links(cap_html)

        n += 1
        fig_id = "fig-#{lang}-#{n}"

        %Q{
<figure id="#{fig_id}" class="md-figure">
  <div class="md-figure-inner">
    #{img_tag}
  </div>
  #{ cap_html.strip.empty? ? "" : %Q{<figcaption class="md-figcaption"><span class="figlabel">#{label} #{n}.</span> #{cap_html}</figcaption>} }
</figure>
        }.strip
      end
    end

    # ------------ utilidades ------------
    def extract_attr(tag, name)
      tag[/\b#{Regexp.escape(name)}="([^"]*)"/i, 1] ||
        tag[/\b#{Regexp.escape(name)}='([^']*)'/i, 1]
    end

    # ALT sin Liquid (para atributo)
    def strip_liquid(s)
      s.to_s.gsub(/\{\%.*?\%\}/m, "").gsub(/\{\{.*?\}\}/m, "").strip
    end

    def h(s)
      s.to_s.gsub("&","&amp;").gsub("<","&lt;").gsub(">","&gt;").gsub('"',"&quot;")
    end

    # {: #id .cls data-x="y" width="60%"} → id="id" class="cls" data-x="y" width="60%"
    # acepta comillas curvas en origen y las normaliza
    def kramdown_attrs_to_html(raw)
      return "" unless raw && !raw.empty?
      s = raw.to_s.strip
      # removes "{:" (kramdown) or "{" (pandoc) and "}"
      s = s.sub(/\A\{\:\s*/, "").sub(/\A\{\s*/, "").sub(/\s*\}\z/, "").strip
      return "" if s.empty?
      s = s.tr("“”’‘", %q{""''})

      classes, id, others = [], nil, []
      tokens = s.scan(/(?:[^\s"']+|"(?:\\.|[^"])*"|'(?:\\.|[^'])*')+/)
      tokens.each do |tok|
        if tok.start_with?("."); classes << tok[1..-1]
        elsif tok.start_with?("#"); id = tok[1..-1]
        else; others << tok
        end
      end

      html = +""
      html << %( id="#{id}") if id && !id.empty?
      html << %( class="#{classes.join(' ')}") if classes.any?
      html << " " + others.join(" ") if others.any?
      html.strip
    end
  end
end

# ---------- Fase 1: Generator (Markdown images) ----------
class ImageCaptionGenerator < Jekyll::Generator
  safe true
  priority :low

  def generate(site)
    coll = site.collections["chapters"]
    return unless coll && coll.docs&.any?
    coll.docs.each do |doc|
      lang  = Jekyll::ImageCaptionTools.detect_lang_code(doc)
      label = Jekyll::ImageCaptionTools.figure_label_for(site, lang)
      doc.content = Jekyll::ImageCaptionTools.transform_markdown_images(doc.content, lang, label)
    end
  end
end

# ---------- Fase 2: Hook post_render (fallback <p><img></p>) ----------
Jekyll::Hooks.register :documents, :post_render do |doc|
  next unless doc.collection&.label == "chapters"
  lang  = Jekyll::ImageCaptionTools.detect_lang_code(doc)
  label = Jekyll::ImageCaptionTools.figure_label_for(doc.site, lang)
  doc.output = Jekyll::ImageCaptionTools.wrap_html_imgs_in_output(doc.output, lang, label)
end
