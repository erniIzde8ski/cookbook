#let prefix(uri) = {
  let match = uri.match(regex("^(\w+)://"))
  if match != none {
    match.captures.at(0)
  }
}


#let is-uri(text) = prefix(text) != none
