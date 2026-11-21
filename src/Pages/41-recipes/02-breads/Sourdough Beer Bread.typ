#import "/prelude.typ": *

#Recipe(
  title: "Sourdough Beer Bread",
  yield: [1 \~1500mℓ loaf#fn[For a round loaf, roughly 20cm or 8" in diameter.

      Unless otherwise specified, all gear used is round or bowl-like, with those
      dimensions, and with a maximum capacity of at least 2000mℓ.]],
  refs: <kabc_beer-bread>,
  description: [A great dipping bread. Goes well with soups like @R_barszcz.],
  {
    [
      Gear:
      - [\*] Dutch oven#fn[A bread steel should, hypothetically, also work. Don't own one;
          don't know.]
      - [\*] Parchment paper
    ]

    let ingredient(
      label,
      grams,
      ml-per-gram,
      fluid: false,
      show-right: true,
      optional: false,
      multiplier: 1,
    ) = {
      grams *= multiplier

      let mLs = grams * ml-per-gram

      let left = [#smartround(grams)g]
      let right = [#smartround(mLs)mL]
      if fluid {
        let copy = left
        left = right
        right = copy
      }

      if optional {
        beside[(optional)~ ]
      }
      [#left #label]
      if show-right {
        [ ]
        aside(right)
      }
    }

    let oat-weight = 141

    let bread-flour-weight = 420

    let starter-weight = 227
    // Amount of water by weight, as a bakers' percentage
    let starter-hydration = 50%
    let starter-ratio = starter-hydration / (starter-hydration + 100%)

    let grain-weight = (
      oat-weight + bread-flour-weight + (1 - starter-ratio) * starter-weight
    )
    // TODO: Would it be easier if we just multiplied by say 1.1 to get nice round metric cups?
    // TODO: cite https://www.aqua-calc.com/calculate/food-weight-to-volume
    let ingredients = (
      "Soaker": (
        ingredient("rolled oats", oat-weight, 2.957),
        ingredient("boiling water", 113, 1, fluid: true, show-right: false),
      ),
      "Dough": (
        ingredient("bread flour", bread-flour-weight, 227.3 / 120),
        ingredient("beer, medium to dark", 255, .994, fluid: true),
        ingredient("sourdough starter, fed", 227, 227 / ((227 + 241) / 2)),
        ingredient("active dry yeast", 6 / 2 * 1.4, 1.232),
        ingredient(
          [dough enhancer#fn[I'm using this one:~ https://www.amazon.com/dp/B00EFFP966\ I
              don't recommend it. The FDA label, or rather, the lack thereof, does not
              look legitimate.]],
          grain-weight * 0.02,
          4 / 2.3,
          optional: true,
        )
          + [ ]
          + CN,
        ingredient("honey", 21, 0.698),
        ingredient("table salt", 0.018 * grain-weight, 0.81),
      ),
    )

    for (header, xs) in ingredients {
      semibold(header + ":")
      for x in xs [- #x]
      parbreak()
    }
  },
)[
  + COMBINE soaker ingredients in medium-small bowl.
  + COVER and set aside.
  + MIX in new bowl until well-combined: flour, beer, starter, yeast, and dough enhancer.
    #pause[1-2 min. on medium-low speed]
  + COVER. #pause[30 min.]
  + MIX soaker & remaining ingredients into dough until combined. #pause[3-4 min. on
      medium-low speed]
  + COVER. #pause[30 min.]
  + PERFORM one round of stretch & folds.
  + COVER. #pause[30 min.]
  + SHAPE dough into circle on round surface.
  + COVER. #pause[20 min.]
  + SHAPE dough into compact boule.
  + FLOUR a brotform.
  + MOVE boule seam-side up to brotform. #pause[1 hour]
  + PREHEAT oven, with dutch oven on center rack, to 230°C. #pause[30 min.; 450°F]
  + INVERT dough onto parchment.
  + SCORE dough several times.
  + MOVE loaf with parchment onto dutch oven.
  + BAKE covered. #pause[15 min.]
  + COOL oven to 200°C. #aside[400°F]
  + BAKE uncovered, until dark brown. #pause[35-40 min.]
  + MOVE loaf to wire rack.
  + COOL loaf to room temperature.
]
