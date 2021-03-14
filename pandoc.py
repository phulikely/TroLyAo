import pypandoc

output = pypandoc.convert_file("readme.md", "epub", outputfile="readme.epub")
assert output == ""