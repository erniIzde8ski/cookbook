#import "/ext.typ": meander
#import "../palette.typ": *
#let Label = label
#let _recipe(
  title,
  label,
  description,
  ingredients,
  yield,
  panel-width,
  steps,
  refs,
) = {
  show regex("^.+:$"): text.with(weight: "semibold")
  let box = box.with(stroke: 0.05em + gray, inset: 0.5em, radius: 0.5em)

  if title != none [
    #title #label
  ]

  if description != none {
    set par(first-line-indent: (all: true, amount: 1.5em))
    description
    v(0.5em)
  }

  meander.reflow({
    import meander: *

    if ingredients != none {
      placed(
        top + left,
        {
          show: box.with(width: panel-width, fill: luma(90%))
          show list: it => it + v(0.5em)
          set text(size: 0.95em)
          ingredients
        }
          + h(1em)
          + v(0.5em),
      )
    }

    if yield != none {
      placed(top + right, {
        show: box.with(width: 100% - panel-width - 1.5em, fill: baby-blue.darken(12%))
        show: align.with(right)
        show: smallcaps
        set text(
          font: ("Ysabeau", "Source Sans Pro", "Bitstream Vera Sans"),
          tracking: 0.06em,
        )
        text(fill: red.lighten(95%), weight: 900)[YIELD:~~]
        yield
      })
    }

    container()
    content({
      steps
    })
  })

  if refs != none {
    [== References]
    if type(refs) == array {
      for lbl in refs {
        parbreak()
        if str(lbl).starts-with("R_") {
          ref(lbl)
        } else {
          cite(lbl, form: "full")
        }
      }
    } else { refs }
  }
}

#let Recipe(
  title: none,
  label: none,
  description: none,
  yield: none,
  refs: none,
  ..args,
  panel-width: auto,
) = {
  let pos = args.pos().rev()

  let _label = label
  let label = none
  for labelable in (_label, title) {
    if type(labelable) == str {
      label = Label(
        "R_" + lower(labelable).replace(" ", "-").replace(regex("[^a-zA-Z_-]"), ""),
      )
      break
    } else if type(labelable) == Label {
      label = labelable
      break
    }
  }
  if type(title) == str {
    // see: https://forum.typst.app/t/label-b-occurs-multiple-times-in-the-document-when-including-outline/7531
    title = [= #title]
  }

  let ingredients = pos.remove(pos.len() - 1, default: none)
  let steps = pos.remove(pos.len() - 1, default: none)

  if type(yield) in (int, float, decimal) {
    yield = fmt("{} serving{}", yield, if yield == 1 { "" } else { "s" })
  }

  if panel-width == auto {
    panel-width = if ingredients == none { 0% } else if steps == none {
      if yield == none { 100% } else { 75% }
    } else { 36% }
  }

  if type(refs) == Label {
    refs = (refs,)
  }

  _recipe(title, label, description, ingredients, yield, panel-width, steps, refs)
}
