import mistune




if __name__ == '__main__':
	your_markdown_text="README.md"
	with open(your_markdown_text,"r",encoding="utf-8") as f,open("README.html","w+",encoding="utf-8") as f1:
		your_markdown_text=f.read()
		c=mistune.html(your_markdown_text)
		f1.write(c)

