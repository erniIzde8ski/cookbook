/// Checks if any value is a numeric type or a numeric-like string
///
/// - val (any):
/// -> boolean
#let __is-numeric(val) = (
  type(val) in (int, float, decimal, ratio)
    or (type(val) == str and val.matches(regex(`^\d+(\.\d+)?$`.text)) != none)
)
#assert(__is-numeric("1.15"))


#let __simplify-decimal(dec) = decimal(str(dec).trim(regex(`\.0*$`.text), repeat: false))
#assert(__simplify-decimal(1600) == decimal("1600"))


/// Simplify a Zlomek.
///
/// - zlomek (dictionary):
/// -> dictionary
#let simplify(zlomek) = {
  let numerator = __simplify-decimal(zlomek.numerator)
  let denominator = __simplify-decimal(zlomek.denominator)

  let mult = (
    {
      (1,)
      for n in (numerator, denominator) {
        let s = str(n)
        let i = s.position(".")
        if i != none {
          (s.len() - i,)
        }
      }
    }.reduce(calc.max)
      - 1
  )

  if mult != 0 {
    mult = calc.pow(10, mult)
    numerator *= mult
    denominator *= mult
  }

  numerator = __simplify-decimal(numerator)
  denominator = __simplify-decimal(denominator)

  let ni = int(numerator)
  let di = int(denominator)
  assert(ni == numerator and di == denominator)

  let gcd = calc.gcd(ni, di)
  ni /= gcd
  di /= gcd
  (numerator: int(ni), denominator: int(di))
}
#simplify((numerator: decimal("1.15"), denominator: decimal("16")))


/// Construct a new Zlomek instance.
///
/// - zlomek (any):
/// -> dictionary
#let new(zlomek) = {
  let zlomek = zlomek

  if __is-numeric(zlomek) {
    zlomek = (numerator: decimal(zlomek), denominator: 1)
  }

  if type(zlomek) == array {
    assert(
      zlomek.len() == 2 and zlomek.all(__is-numeric),
      message: "Array input to `Zlomek.new` should be a pair of numeric values.",
    )
    let (n, d) = zlomek.map(decimal)
    zlomek = (numerator: n, denominator: d)
  }

  if type(zlomek) == dictionary and "denominator" not in zlomek {
    zlomek.denominator = 1
  }

  assert(
    type(zlomek) == dictionary
      and zlomek.keys().sorted() == ("denominator", "numerator")
      and zlomek.values().all(__is-numeric),
    message: "Input to function `Zlomek.new` should be numeric, a pair of numerics, or a
      record of type `{ numerator: numeric, denominator?: numeric }`.",
  )

  if type(zlomek.numerator) == str {
    zlomek.numerator = decimal(zlomek.numerator)
  }
  if type(zlomek.numerator) == decimal {
    let s = str(zlomek.numerator)
    let parts = s.split(".")
  }

  assert(zlomek.denominator != 0, message: "Denominator cannot equal zero")

  simplify(zlomek)
}

#assert(new(("1.5", "4.5")) == (numerator: decimal(1), denominator: decimal(3)))


#let neg(zlomek) = {
  let zlomek = new(zlomek)
  return new((-1 * zlomek.numerator, zlomek.denominator))
}
#assert(neg(-2) == (numerator: 2, denominator: 1))


#let add(augend, addend) = {
  let augend = new(augend)
  let addend = new(addend)
  let d = calc.lcm(augend.denominator, addend.denominator)
  let ln = augend.numerator * d / augend.denominator
  let rn = addend.numerator * d / addend.denominator
  let n = ln + rn
  assert(n == int(n))
  new((n, d))
}
#assert(add((1, 2), (1, 3)) == (numerator: 5, denominator: 6))


#let sub(minuend, subtrahend) = add(minuend, neg(subtrahend))


#let sum(..args) = args.pos().reduce(add)


#let inverse(zlomek) = {
  let z = new(zlomek)
  new((z.denominator, z.numerator))
}
#let inv = inverse


/// - left (dictionary): a zlomek
/// - right (dictionary): a zlomek
/// -> dictionary
#let mult(left, right) = {
  let left = new(left)
  let right = new(right)
  new((left.numerator * right.numerator, left.denominator * right.denominator))
}
#assert(mult((1, 3), (1, 3)) == (numerator: 1, denominator: 9))


#let divide(dividend, divisor) = {
  let dividend = new(dividend)
  let divisor = new(divisor)

  return mult(dividend, inverse(divisor))
}
#let div = divide
#assert(divide(1, 3) == (numerator: 1, denominator: 3))


#let prod(..args) = args.pos().reduce(mult)
#assert(prod((1, 2), (3, 4), (5, 6)) == new((15, 48)))
