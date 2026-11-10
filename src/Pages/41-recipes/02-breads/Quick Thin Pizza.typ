#import "/prelude.typ": *

#show: Recipe.with(
  title: "Quick Thin Pizza",
  description: [
    Quickly-prepared pizza with a thin crust. Adapted from a recipe by PJ
    Hamel:~https://www.kingarthurbaking.com/recipes/super-fast-thin-crust-pizza-dough-recipe
  ],
  panel-width: 40%,
  yield: [1 large pizza],
)[
  Dough:
  - 150mℓ water, warm
  - 8g active dry yeast #pause[10mℓ]
  - 35g olive oil #pause[37mℓ]
  - 3mℓ basil, dried
  - 3mℓ oregano, dried
  - 3mℓ marjoram, dried
  - 5--7g salt #aside[4--6mℓ]
  - 6g Easy Roll Dough Improver #aside[optional]
  - 40g einkorn flour #aside[80mL]
  - 200g all-purpose flour #footnote[~00 Pizza Flour should, theoretically, provide better
      results. Bread flour is OK, but not advisable; produces a chewy pizza.]
    #aside[395mL]


  Recommended toppings:
  - Tomato sauce
  - Shredded mozzarella
  - Turkey pepperoni
]

#let sep = v(0.35em)
+ #RI.PREHEAT(obj: "oven (with pizza stone or steel)", spacer: aside, temperature: 450)
+ MIX dough in order: water & yeast; oil; remaining ingredients.
+ COVER dough. #pause[25 min.]
+ FLATTEN tiny tiny crust onto parchment paper.
+ ADD toppings to crust.
+ BAKE with paper set directly atop pizza stone. #pause[9-12 min.]
+ REST before cutting. #pause[3 min.]
