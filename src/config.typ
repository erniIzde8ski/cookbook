#let _I = sys.inputs
#let release-mode = {
  let val = _I.at("mode", default: "debug")
  if val == "release" { true } else if val == "debug" { false } else {
    panic(
      `input argument 'mode' must be either "debug" or "release"; received "`.text
        + val
        + "\"",
    )
  }
}
#let debug-mode = not release-mode

#let author = if release-mode { "Ernie Izdebski" } else { "Erni Izdebski" }
#let title = "Cookbook 2"
