/// Determines if an object appears to be an empty or zero-ish value.
///
/// - obj (any): object to check
/// -> bool: falsiness of the `obj`
#let is-falsy(obj) = (
  obj
    in (
      none,
      false,
      0,
      decimal("0"),
      0.0,
      float("NaN"),
      0%,
      "",
      (),
      (:),
      [],
      [ ],
    )
)


/// Determines if an object appears to be a non-empty & non-zero value.
///
/// - obj (any): object to check
/// -> bool: truthiness of the `obj`
#let is-truthy(obj) = not is-falsy(obj)


#let supports-numbering(it) = type(it) == content and it.func() != bibliography


#let has-numbering(it) = supports-numbering(it) and it.numbering != none

#assert(not has-numbering(none))
#assert(not has-numbering(heading(numbering: none)[foo]))
#heading(numbering: "1.")[foo].func()
#assert(has-numbering(heading(numbering: "1.")[foo]))
