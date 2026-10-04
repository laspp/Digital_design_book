-- For LaTeX/PDF output, swap generated images/{waves,blocks}/*.svg for the
-- matching .pdf (made by scripts/render_waves.py and render_blocks.py),
-- so no rsvg-convert is needed.
function Image(img)
  if FORMAT:match("latex") and (img.src:match("^images/waves/.*%.svg$")
      or img.src:match("^images/blocks/.*%.svg$")) then
    img.src = img.src:gsub("%.svg$", ".pdf")
    return img
  end
end
