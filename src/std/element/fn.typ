#import "../palette.typ": *
#import "/config.typ": debug-mode

#let _super = super
#let _no-op(val) = val

/// Returns superscript (by default) red text marking missing content.
///
/// - thing (any): name of thing needed
/// - super (bool): render using superscript
/// -> content
#let missing(thing, super: true) = if debug-mode {
  let thing = [[#thing needed]]
  if super { thing = _super(thing) }

  set text(fill: red)
  thing
}

#let blockquote = quote.with(block: true)
#let semibold = text.with(weight: "semibold")

#let checklist = {
  import "@preview/cheq:0.4.0": *

  let marker = text.with(baseline: -0.1em)

  checklist.with(
    extras: true,
    marker-map: (
      ".": marker(sym.dot.c + h(0.10em)),
      "*": marker(sym.ast, size: 0.8em),
    ),
  )
}

#let mdtable = {
  import "@preview/tablem:0.3.0": three-line-table
  three-line-table.with(fill: (_, y) => if calc.odd(y) { pale-blue })
}


#let invisible(body) = hide(place(body, float: false))

#let HR(length: 50%) = {
  set align(center)
  show: pad.with(y: 0.5em)
  line(length: 50%)
}

#let beside(body) = {
  set text(style: "italic", weight: 600, size: 0.85em, fill: luma(20%))
  body
}

#let aside(body, left: "(", right: ")") = beside[~~#left#body#right]

#let pause-spacer = v(0.50em)
#let pause(body) = aside(body) + pause-spacer
