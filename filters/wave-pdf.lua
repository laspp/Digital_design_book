-- For LaTeX/PDF output, swap every images/**/*.svg for the matching .pdf
-- (made by scripts/render_*.py with cairosvg), so no rsvg-convert is needed.
function Image(img)
  if FORMAT:match("latex") and img.src:match("^[./]*images/.*%.svg$") then
    img.src = img.src:gsub("%.svg$", ".pdf")
    return img
  end
end
