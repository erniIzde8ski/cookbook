#let title-case(string) = (
  string.split().map(it => upper(it.at(0)) + lower(it.slice(1))).join(" ")
)


/// Converts some content to a string. Panics on failure.
///
/// - key (content): The content to convert to string.
/// -> string
#let from-content(key) = {
  if type(key) == str {
    key
  } else if type(key) == content {
    if key == smartquote(double: false) {
      return "'"
    } else if key == smartquote(double: true) {
      return "\""
    }
    key.fields().values().flatten().map(from-content).join("")
  } else if type(key) == label {
    return repr(key)
  } else {
    panic("unsupported type: " + repr(key))
  }
}
