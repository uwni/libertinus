#set text(font: "Libertinus Serif", size: 40pt)

#for font in ("New Computer Modern Math", "Libertina Math", "Libertinus Math") [
  #show math.equation: set text(font: font)
  #block(stroke: red)[$
    a^b sin (b^b^b + y) dif x
  $]

  #for (ssty, color) in ((0, red), (1, green), (2, blue)) {
    show: it => context measure(it).height
    text(features: (ssty: ssty), $o$, stroke: 0.01em + color, fill: white.transparentize(100%), top-edge: "bounds", bottom-edge: "bounds")
  }
]
