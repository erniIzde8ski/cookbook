#let Footnote = footnote

#let footnote(body) = Footnote[~#body]
#let fn = footnote

#let Footnotes = {
  import "common-urls.typ": url

  (
    allspice: [Allspice tastes of cinnamon, cloves, and nutmeg@hos2_allspice; it doesn't
      add a _new_ flavor.],
    bean-expansion: [Dry beans expand to 2-3 times their size.],
    bean-seasoning: [#url[Chicken bouillon] works even better! Toss in your favorite
      seasonings. Sometimes I like assorted Italian seasoning, onion powder, garlic
      powder, or cloves of garlic.],
    bean-soaking: [While you don't _have_ to soak your beans, it may help your beans cook
      more consistently.],
    bean-stinking: [Beans will get stinky after more than a day or two of soaking.],
    cream: [Americans: #url[Cream], not #url[sour cream]!],
    cumin: [Be VERY careful with cumin. A pinch too much of salt? Salty, but you'll
      survive. A pinch too much of cumin? Completely inedible.],
    erdi: [I buy this specific dough improver from King Arthur Baking
      Company:~#[https://shop.kingarthurbaking.com/items/easy-roll-dough-improver]. Adjust
      hydration if you forgo it.],
    fry-basket: [I recommend a fry basket. I own this
      one:~https://www.amazon.com/dp/B001VZARVK],
    food-processor: [You can technically get away with a blender, but it's a hell of a lot
      more tedious.],
    grease-keeper: [If lacking a #url(key: "grease keeper")[fine-mesh grease keeper], a
      fine-mesh strainer & a 4ℓ bucket will do just fine.],
    liquid-hickory: [Careful with hickory smoke! Delicious flavor, but it's extremely
      bitter.],
    piloncillo: [Piloncillo substitutes 1-to-1 with brown sugar, particularly unrefined.],
    rice-cooker: [My rice cooker cooks up to 12 cups.],
    sodium-citrate: [Sodium citrate is a cheese emulsifier; that is, it helps keep cheese
      molecules bound to water molecules. It's also somewhat saline, so you get to use
      less salt when you use it.],
    the-texture-destroyer: [Just don't boil it. I trust you.],
  ).map(fn)
}

#let Fn = Footnotes
