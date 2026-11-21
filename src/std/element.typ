#import "element/RecycledInstruction.typ"
#import "element/RecycledInstruction.typ" as RI
#import "element/fn.typ": HR
#import "element/fn.typ": aside
#import "element/fn.typ": beside
#import "element/fn.typ": blockquote
#import "element/fn.typ": blockquote as bq
#import "element/fn.typ": checklist
#import "element/fn.typ": checklist
#import "element/fn.typ": invisible
#import "element/fn.typ": laside
#import "element/fn.typ": mdtable
#import "element/fn.typ": missing
#import "element/fn.typ": pause
#import "element/fn.typ": pause-spacer
#import "element/fn.typ": semibold
#import "element/fn.typ": semibold as sb
#import "element/placeholder.typ": Placeholder
#import "element/recipe.typ": Recipe

#let CN = missing[citation]
#let VN = missing[volume]
#let WN = missing[weight]

/// -> content
#let V = {
  set align(center)
  v(1em)
  line(length: 50%)
  v(1em)
}
#let LS = v(0.5em)
#let hr = HR()

#let list-break = v(0.25em)
#let lsb = list-break
