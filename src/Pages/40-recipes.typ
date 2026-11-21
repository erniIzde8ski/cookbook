#import "/prelude.typ": title-case


#let mkrecipechapter(title, offset: 1) = box(
  {
    set align(center + horizon)
    set text(size: 1.5em)
    set heading(offset: offset)
    title
  },
  width: 100%,
  height: 100%,
)

#let BASE_PATH = "./41-recipes/"
#let RECIPES = yaml(BASE_PATH + "index.yaml")

#let mkrecipe(path, base-path: BASE_PATH) = {
  let path = base-path + path

  show heading.where(depth: 1): it => {
    [#counter(footnote).update(0)]
    align(center, it)
  }
  set heading(offset: 2)

  show footnote.entry: set text(0.85em)

  show ref: lower

  show regex(" ?1/8"): "⅛"
  show regex(" ?1/4"): "¼"
  show regex(" ?1/3"): "⅓"
  show regex(" ?3/8"): "⅜"
  show regex(" ?1/2"): "½"
  show regex(" ?5/8"): "⅝"
  show regex(" ?3/4"): "¾"
  show regex(" ?5/6"): "⅚"
  show regex(" ?7/8"): "⅞"
  show regex(`(?:\b|\d)[kmµ]?L\b`.text): it => {
    show "L": "ℓ"
    it
  }

  include path
}

#{
  mkrecipechapter([= Recipes <recipes>], offset: 0)

  pagebreak()

  // don't worry about it
  let Chapter = regex("(?:^|/)(?:\\d+-)([a-zA-Z]+)/$")
  for recipe in RECIPES {
    let chapter = recipe.match(Chapter)
    if chapter != none {
      let title = title-case(chapter.captures.at(0))
      mkrecipechapter([= #title])
    } else {
      mkrecipe(recipe)
    }
    pagebreak()
  }
}
