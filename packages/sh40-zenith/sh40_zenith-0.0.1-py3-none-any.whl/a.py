from zenith import Palette, markup

palette = Palette.from_hex("#4A7A9F")
palette.alias()
print(markup(palette.render()))

print(markup("[primary-2]Primary foreground color, darkened twice"))
