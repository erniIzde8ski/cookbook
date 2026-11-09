#import "/config.typ"

// TODO: Add section headers
#let mkpgheader(gap: 0.5em) = none

#let mkpgfooter(gap: 0.5em) = context {
  let page-display = counter(page).display("1 of 1", both: true)
  let sep = {
    h(gap)
    [---]
    h(gap)
  }
  page-display = {
    sep
    page-display
    sep
  }

  if page.width < 40em.to-absolute() {
    return align(end, page-display)
  }

  import "/std/format.typ": format-date

  let page-no = counter(page).get().at(0)

  let (l, r) = if calc.rem-euclid(page-no, 2) == 0 {
    (page-display, [#format-date(datetime.today())])
  } else {
    (
      {
        quote(document.title)
        if config.debug-mode [~(dev copy)]
      },
      page-display,
    )
  }

  columns(2, {
    align(left, l)
    colbreak()
    align(right, r)
  })
}

#let mkbook(
  title: config.title,
  page-size: "us-letter",
  page-header: true,
  page-footer: true,
) = {
  import "./format.typ": format-document

  set document(
    author: config.author,
    title: config.title,
  )

  set page(
    header: if page-header { mkpgheader() },
    footer: if page-footer { mkpgfooter() },
  )

  show: format-document(page-size: page-size)

  let pages = (
    include "/Pages/10-cover.typ",
    include "/Pages/20-outline.typ",
    include "/Pages/30-advice.typ",
    include "/Pages/40-recipes.typ",
    include "/Pages/50-appendix.typ",
    include "/Pages/60-references.typ",
  )

  pages.join(pagebreak(weak: true))
}
