#import "/ext.typ"

#let assert-eq(left, right) = {
  import ext.oxifmt: strfmt

  assert(left == right, message: strfmt("assertion failed: {:?} == {:?}", left, right))
}
