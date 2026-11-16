#import "String.typ"
#import "uri.typ"
#import "utils.typ"


#let normalize-key(key) = {
  if type(key) != str {
    return none
  }
  lower(
    key.trim().replace(regex("(\s|-)+"), "-").replace(regex("[^a-zA-Z-]"), ""),
  )
}

#let URL = (
  chicken-bouillon: "https://www.amazon.com/Knorr-Chicken-Flavor-Bouillon-35-3/dp/B0711K2YP7",
  grease-keeper: "https://www.amazon.com/Oggi-7347-Jumbo-Grease-Stainless/dp/B0711FN8BG",
  pullman-loaf-pan: "https://shop.kingarthurbaking.com/items/pullman-loaf-pan",
  baking-steel: "https://alexandracooks.com/2020/05/01/simple-sourdough-pizza-a-step-by-step-guide/",
  sodium-citrate: "https://www.amazon.com/dp/B07NF4B3Y7",
  cream: "https://en.wikipedia.org/wiki/Cream",
)


#let url(display, key: auto) = {
  if key == auto { key = display }
  key = String.from-content(key)
  if uri.is-uri(key) {
    return link(key, display)
  }
  key = normalize-key(key)
  let url = URL.at(key, default: none)
  if url == none {
    text(display, fill: red)
  } else {
    link(url, display)
  }
}
