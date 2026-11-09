#import "@preview/oxifmt:1.0.0": strfmt as format

#let fmt = format

#let format-date(date) = fmt(
  "{year:<04}-{month:<02}-{day:<02}",
  year: date.year(),
  month: date.month(),
  day: date.day(),
)

#let format-document(
  page-size: "us-letter",
  uri-default: blue,
  uri-label: green.darken(20%),
  uri-insecure: red,
  bg: white,
  bg-dim: luma(80%),
) = body => context {
  import "/std/size-mult.typ"
  import "Dimensions.typ"
  import "Emoji.typ"
  import "element.typ": checklist
  import "element.typ": list-break
  import "utils.typ": has-numbering
  import "utils.typ": supports-numbering

  let page-args
  if type(page-size) == str {
    page-args = Dimensions.USER_DEFINED.at(page-size, default: (page-size,))
  } else {
    page-args = page-size
  }
  set page(..page-args, margin: (x: 7%, y: 7%))

  show: body => context {
    // 41.7 with my phone, 78.6 with `us-letter`
    let size = calc.pow(page.width.pt() * page.height.pt(), 1 / 3)
    let multiplier = size-mult.ratio(page)

    set text(
      font: ("Twitter Color Emoji", "Libertinus Serif"),
      size: 12pt * size / 78.6,
    )

    body
  }

  set underline(evade: true)

  show raw.where(block: false): it => {
    show: box.with(
      fill: bg-dim,
      radius: 25%,
      outset: (bottom: 3pt, top: 2pt),
      inset: (x: 2pt),
    )
    it
  }

  show raw.where(lang: "hayagriva"): it => bibliography(bytes(it.text))

  set pagebreak(weak: true)

  show: checklist
  show: Emoji.use-syntax

  let OUTLINE_DEPTH = state("PREV_OUTLINE_DEPTH", none)
  show outline.entry: it => context {
    // In Typst v0.14, these default to 0.55em and 1em
    let above = block.above
    let below = block.below

    if it.level == 1 {
      above = 140em / 100
    } else if it.level == 2 {
      above = 80em / 100
    }

    set block(above: above, below: below)
    it
  }

  set par(
    first-line-indent: 0em,
    spacing: 0.85em,
    leading: 0.35em,
    // We don't usually use justified text, but if/when we do, character-level
    // justification is a HUGE boon.
    justification-limits: (
      tracking: (min: -0.01em, max: 0.02em),
    ),
  )
  set text(region: "US")
  set enum(spacing: 0.55em)
  set list(marker: text(baseline: -0.06em)[---], body-indent: 0.35em)

  show heading.where(depth: 1): set text(size: 1.5em)
  show heading: it => {
    let text-size = 1em
    if it.depth < 2 {
      it = underline(it)
      text-size = 1.50em
    } else if it.depth == 2 {
      text-size = 1.35em
    } else if it.depth == 3 {
      text-size = 1.08em
    } else {
      it = {
        set text(style: "italic")
        it
      }
    }
    set text(size: text-size)
    link(<outline>, it)
  }
  show heading.where(level: 4): set heading(outlined: false)
  show heading.where(level: 5): set heading(outlined: false)
  show heading.where(level: 6): set heading(outlined: false)

  show ref: it => {
    let elem = it.element

    if it.form == "page" {
      return context {
        let page-no = locate(it.citation.key).page()
        [pg. #page-no]
      }
    }

    if not supports-numbering(elem) or has-numbering(elem) {
      return it
    }

    let body = it.supplement
    if it.supplement == auto {
      body = elem.body
    }
    // `type(elem) == content`, not `heading`
    show: link.with(it.citation.key)
    underline(body)
    [ (#ref(it.citation.key, form: "page"))]
  }
  show link: it => {
    if it.dest == <outline> {
      return it
    }

    let color = uri-default
    let _underline = false

    if type(it.dest) == label {
      color = uri-label
    } else if type(it.dest) == str {
      if it.dest.starts-with("http://") {
        color = uri-insecure
      } else {
        _underline = true
      }
    }

    set text(fill: color)
    if _underline { underline(it) } else { it }
  }
  set footnote(numbering: "(1)")
  show footnote.entry: set text(0.85em)

  show regex("^-\|$"): list-break

  set enum(numbering: "1.A.I.i.")

  show quote.where(block: true): set block(above: auto, below: auto)
  show quote.where(block: true): box.with(
    inset: (left: 0.5em),
    stroke: (left: 2pt + gray),
  )

  set bibliography(title: "References", style: "american-chemical-society")

  body
}
