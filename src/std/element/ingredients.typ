#import "../footnotes.typ": fn as _fn
#let _group(xs) = {
  for x in xs [- #x]
  parbreak()
}
#let Groups(..items) = {
  _group(items.pos())

  for (name, xs) in items.named() {
    text(name + ":", weight: "semibold")
    _group(xs)
  }
}

#let _new(
  default-name,
  ml-per-gram,
  liquid: false,
  multiplier: 1,
  show-right: true,
  default-optional: false,
) = (grams, optional: default-optional, display: default-name) => {
  import "/prelude.typ": *

  grams *= multiplier

  let mLs = grams * ml-per-gram

  let left = [#smartround(grams)g]
  let right = [#smartround(mLs)mL]
  if liquid {
    let copy = left
    left = right
    right = copy
  }

  if optional {
    beside[(optional)~ ]
  }
  [#left #display]
  if show-right {
    [ ]
    aside(right)
  }
}


/* LIQUIDS */
#let _new-lick = _new.with(liquid: true)

#let beer-medium = _new-lick("beer, medium", .994)

#let milk = _new-lick("milk", .970)
#let milk-whole = milk.with(default-name: "whole milk")

// water at room temperature is ever-so-slightly larger than 1mℓ per gram
#let water = _new-lick("water", 1.002, show-right: false)
#let water-boiling = water.with(display: "boiling water")


/* MUSHY STUFF */
#let honey = _new("honey", 0.698)
#let starter = _new("sourdough starter", 227.3 / ((227 + 241) / 2))


/* GRAINS & FLOURS */
#let rolled-oats = _new("rolled oats", 2.838)
#let bread-flour = _new("bread flour", 227.3 / 120)


/* MIXES & POWDERS */
#let (active-yeast, instant-yeast) = {
  // guess who doesn't actually own instant dry yeast lol
  let ratio = 1.232
  let it = _new.with("active-dry yeast", 1.232)
  (it(), it(multiplier: 4 / 3))
}
#let dough-enhancer = _new(
  [dough enhancer#_fn[I'm using this one:~ https://www.amazon.com/dp/B00EFFP966\ I don't
      recommend it. The FDA label, or rather, the lack thereof, does not look
      legitimate.]],
  4 / 2.3, // TODO: verify
  default-optional: true,
)
#let salt = _new("table salt", 0.81)
