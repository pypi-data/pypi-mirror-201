from jinja2 import Environment, FileSystemLoader

env = Environment(
    loader=FileSystemLoader("templates"), trim_blocks=False, lstrip_blocks=False, keep_trailing_newline=True
)

head = env.get_template("head.j2.f")
head_render = head.render()

body = env.get_template("block.j2.f")
body_render = body.render(start="if", c1="x", c2="y", p1=10, p2=20, r=10, load=20)

render = head_render + "\n" + body_render

with open("test.f", mode="w", encoding="utf-8") as f:
    f.write(render)
