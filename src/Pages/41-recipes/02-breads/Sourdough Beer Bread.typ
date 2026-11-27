#import "/prelude.typ": *

#Recipe(
  title: "Sourdough Beer Bread",
  yield: [1 \~1500mℓ loaf #WN #fn[For a round loaf, roughly 20cm or 8" in diameter.

      Unless otherwise specified, all gear used is round or bowl-like, with those
      dimensions, and with a maximum capacity of at least 2000mℓ.]],
  refs: <kabc_beer-bread>,
  description: [A dipping bread. Goes well with soups like @R_barszcz.],
  {
    import ingredients: *

    let oat-weight = 141

    let bread-flour-weight = 420

    let starter-weight = 227
    // Amount of water by weight, as a bakers' percentage
    let starter-hydration = 50%
    let starter-ratio = starter-hydration / (starter-hydration + 100%)

    let grain-weight = (
      oat-weight + bread-flour-weight + (1 - starter-ratio) * starter-weight
    )

    // TODO: Would it be easier if we just multiplied by, say, 1.1 to get nice round metric cups?
    Groups(..(
      Gear: (
        [[\*] Dutch oven#fn[A bread steel should, hypothetically, also work. Don't own
            one; don't know.]],
        [[\*] Parchment paper],
      ),
      Soaker: (rolled-oats(oat-weight), water-boiling(113)),
      "Dough base": (
        beer-medium(255, display: [beer, medium or dark]),
        bread-flour(bread-flour-weight),
        dough-enhancer(grain-weight * 0.02) + [ #CN],
        starter(starter-weight),
        instant-yeast(3),
      ),
      "The rest": (
        honey(21),
        salt(grain-weight * 0.018),
      ),
    ))
  },
)[
  + COMBINE soaker ingredients in medium-small bowl.
  + COVER and set aside.
  + MIX dough base in new bowl until well-combined.
    #pause[1-2 min. on medium-low speed]
  + COVER. #pause[30 min.]
  + MIX soaker & the rest into dough until combined. #pause[3-4 min. on medium-low speed]
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
  + COOL loaf to room temperature. #missing[duration]
]
