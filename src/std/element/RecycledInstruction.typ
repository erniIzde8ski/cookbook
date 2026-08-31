#import "/core/calc.typ"
#import "fn.typ" as _fn


#let PREHEAT(obj: none, temperature: none, unit: "F", space: _fn.pause-spacer) = {
  let nearest-five(n) = calc.round-to-multiple(n, 5)

  let (celsius, fahrenheit) = if temperature == none { (none, none) } else if (
    type(temperature) in (int, float)
  ) {
    if unit == "F" {
      (nearest-five((temperature - 32) / 1.8), nearest-five(temperature))
    } else if unit == "C" {
      (
        nearest-five(temperature),
        nearest-five(temperature * 1.8 + 32),
      )
    } else {
      panic("unsupported unit: " + repr("F"))
    }
  } else {
    panic(
      "invalid argument: parameter `temperature` of `PREHEAT` should be `none`, `int`,
    or `float`; got "
        + repr(type(temperature)),
    )
  }

  assert(
    temperature == none or type(temperature) in (int, float),
    message: "field `temperature` must be `none`, `int`, or `float`, not "
      + repr(type(temperature)),
  )

  [PREHEAT]
  if obj != none [~#obj]
  if temperature != none [, #celsius°C]
  [.]
  if temperature != none { _fn.aside[#fahrenheit°F] }
  space
}

#{
  PREHEAT(obj: "oven", temperature: 180)
}
