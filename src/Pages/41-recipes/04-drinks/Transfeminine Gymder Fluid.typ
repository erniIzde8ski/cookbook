#import "/prelude.typ": *
#import "/config.typ": debug-mode, release-mode

#let SERVINGS = 263

#let dezlomek(it) = {
  if type(it) == dictionary and ("numerator", "denominator").all(key => key in it) {
    return it.numerator / it.denominator
  } else {
    return it
  }
}
#let smartround(f) = calc.round(f, digits: if f < 1 { 2 } else if f < 10 { 1 } else { 0 })
#let smartround-grams(m) = {
  let m = dezlomek(m)
  if m < 1.0 [#smartround(m * 1000);mg] else [#smartround(m);g]
}
#let smartround-mg(m) = smartround-grams(dezlomek(m) / 1000)

/// Weights: mg of <substance> needed per liter of water
#let W = {
  let W = ()

  let Z = Zlomek
  let round = calc.round.with(digits: 0)

  let Substance(
    element,
    raw-form,
    elem-mg-per-fluid-mℓ,
    elem-mg-per-raw-mg,
    include-footnote: debug-mode,
    product: none,
  ) = {
    // element (g) versus fluid (ℓ)
    let elem-water-ratio = Z.new(elem-mg-per-fluid-mℓ)
    // element (g) versus its raw form (g)
    let elem-raw-ratio = Z.new(elem-mg-per-raw-mg)

    // Raw element (g) / fluid (ℓ)
    let raw-mass = Z.div(elem-water-ratio, elem-raw-ratio)
    // Raw element (mg) / fluid (ℓ)
    let raw-mass_m = Z.mult(raw-mass, 1000)

    let explainer = if include-footnote {
      let elem-mass_d = smartround-grams(elem-water-ratio)
      let raw-mass_d = smartround-grams(raw-mass)
      let elem-mass_d = smartround-grams(elem-raw-ratio)
      fn({
        [This makes for about #elem-mass_d of #element (#raw-mass_d raw substance) per
          liter, assumingly roughly #elem-mass_d of #element per gram of #raw-form.]
        if product != none [\ Referenced product: #product]
      })
    }

    let r = [#raw-form#explainer]
    (r, raw-mass_m)
  }

  W.push(Substance(
    "sodium",
    "table salt",
    (430, 625),
    (393, 1000),
  ))

  W.push(Substance(
    "magnesium",
    "lemon-flavored magnesium diglycinate",
    (30, 625),
    (250, 4500),
    product: link(
      "https://www.walgreens.com/store/c/walgreens-magnesium-glycinate-powder-lemon/ID=300455406-product",
    )[Walgreens Magnesium Glycinate Powder Lemon],
  ))

  W.push(Substance(
    "glucose-equivalent sweetness",
    "sucralose",
    (31 * 1000, 625), // we want the equivalent of 31 grams of sugar lmfao
    (600, 1), // sucralose is awful potent
    // include-footnote: false,
  ))

  W.push(Substance(
    "calcium",
    "calcium citrate",
    (50, 650),
    (500 * 18, 25950),
    product: [#link(
        "https://www.walgreens.com/store/c/walgreens-calcium-citrate-500-mg-tablets-(100-days)/ID=300437334-product",
      )[Walgreens Calcium Citrate 500 mg Tablets], crushed into powder with their #link(
        "https://www.walgreens.com/store/c/walgreens-pill-crusher/ID=prod6328102-product?criteria=Recently+Viewed+Items&position=3&wic=932130",
      )[pill crusher]. Each pill weighs about 1.44 grams.],
  ))

  W.sorted(key: ((_, z)) => -z.numerator / z.denominator)
}

#let grams-per-serving = {
  let z = W.map(it => it.at(1)).reduce(Zlomek.add)
  (z.numerator / z.denominator) / 1000
}



#Recipe(
  title: if release-mode { "The Energy Drink" } else { "Transfeminine Gymder Fluid" },
  description: [A potassium-free energy drink formulation. Inspired by Electrolit, Green
    Apple flavor.],
  yield: [#SERVINGS liters\
    (\~#smartround(grams-per-serving)g dry mix per L)],
  for (key, mg) in W {
    let g = mg.numerator / mg.denominator / 1000
    g *= SERVINGS
    let digits = if g < 1 { 2 } else if g < 10 { 1 } else { 0 }
    g = calc.round(g, digits: digits)
    [- #g;g #key]
  },
)[
  + BLEND powderized ingredients together.
  + SIFT into storage container.
  + SHAKE well. \ \ // ugly hack
  + ADD #smartround(grams-per-serving)g (\~$1/2$ tsp.) of powder per 1L of water.
]

== Trivia

#if debug-mode [
  Transgender women often take the anti-androgen spironolactone, which also acts as a
  potassium-preserving diuretic. Essentially, electrolytes go into body, potassium stays
  in, everything else gets flushed out. For gymgoers, an energy drink that does not
  feature potassium can thus prove very helpful.
]

#let safetyLimit = 15
#let sucraloseGrams = 47.7
#let weightEstimate = 60
Because we use sucralose in place of sugar, there are safety limits. At time of writing,
we call for #sucraloseGrams milligrams of sucralose per liter of fluid, and the EFSA & the
FDA advise that individuals consume no more than #safetyLimit milligrams of sucralose per
kilogram of body weight per day. That is to say, if you weigh #weightEstimate kilograms,
you should consume no more than $(weightEstimate times safetyLimit)/sucraloseGrams
= #{ calc.round(weightEstimate * safetyLimit / sucraloseGrams, digits: 1) }#[~] frac("L", "day", style: "skewed")$
of this stuff a day on average.

#if release-mode [
  Neither this recipe nor any claims made herein have been reviewed by the FDA or any
  other health organizations; you prepare this product at your own risk.
]
