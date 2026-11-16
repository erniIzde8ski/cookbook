#let from-diagonal-length(
  diagonal-length,
  pixel-height,
  pixel-width,
) = {
  let c-squared = calc.pow(pixel-height, 2) + calc.pow(pixel-width, 2)
  let c = calc.sqrt(c-squared)
  let distance-per-pixel = diagonal-length / c
  (height: pixel-height * distance-per-pixel, width: pixel-width * distance-per-pixel)
}

#let from-ppi(ppi, pixel-height, pixel-width) = (
  height: pixel-height / ppi * 1in,
  width: pixel-width / ppi * 1in,
)

#let USER_DEFINED = (
  "Kobo Clara": from-diagonal-length(6in, 1448, 1072),
  "Kobo Libra": from-diagonal-length(7in, 1680, 1264),
  "iPhone 16e": from-ppi(460, 2532, 1170),
)
