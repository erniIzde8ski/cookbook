#import "/prelude.typ": *

// #let round-step(num, step: 5) = calc.round(num / step) * step

#Recipe(title: "Baguettes", yield: "2-4 loaves", refs: <kabr_baguettes>)[
  // For some reason, King Arthur Baking uses Canadian cups, so this is a bit
  // smaller than you might expect.
  Pre-ferment:
  - 115mℓ water
  - EITHER: 200mg instant yeast #aside[350µℓ] \
    OR: 25g sourdough starter #aside[15mℓ]
  - 120g all-purpose flour #aside[230mℓ]
  - 5g Easy Roll Dough Improver #aside[optional]

  Dough:
  - Pre-ferment (above)
  - 255mℓ water
  - 5g instant yeast #aside[7mℓ]
  - 420g all-purpose flour #aside[800mℓ]
  - 12g salt #aside[9mℓ]
][
  + MIX pre-ferment ingredients roughly.
  + COVER at room temperature. #pause[12-16 hr.]
  + ADD ingredients to bowl in listed order.
  + MIX thoroughly. #footnote[With a KitchenAid stand mixer, \~4 minutes on speed 2.]
  + TWICE:~
    + COVER in greased bowl. #pause[45 min.]
    + DEFLATE.
  + SLICE dough on greased surface into 2-4 equal parts.
  + FOR each part:~
    + FLATTEN slightly.
    + FOLD in half.
    + ROTATE 180°.
    + REPEAT previous steps.
    + ROLL into log.#footnote[For 2-3 baguettes, I recommend 40cm logs. For 4
        demi-baguettes, 20cm.]
    + ADD log seam-side down to greased baking tray or couche.
  + #RI.PREHEAT(
      obj: "oven with pot & cast-iron on bottom rack",
      space: none,
      temperature: 450,
    )
  + COVER logs until slightly puffy. #pause[45-60 min.] // TODO: Use King Arthur
  // Baking's term "marshmallowy", and add a glossary/glossary entry
  + BOIL 350mℓ of water. #aside[async.]
  + SCORE loaves.
  + ADD loaves to middle rack of oven, then boiling water to cast-iron pot.
  + BAKE until deeply golden-brown. #pause[24-28 min.]
  + STOP oven.
  + IF making crispy baguettes:~
    + OPEN oven slightly ajar. #aside[\~5cm]
    + WAIT until baguettes are room temperature. #missing[duration]
    ELSE:~
    + COOL on wire rack.
]
