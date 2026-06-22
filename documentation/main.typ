#set text(font: "Libertina Serif", size: 20pt)

#for font in ("Libertina Math", "Libertinus Math", "New Computer Modern") [
  #show math.equation: set text(font: font)
  #block(stroke: red+0.01em)[$
   integral epsilon mu epsilon'
  $]

  // #for (ssty, color) in ((0, red), (1, green), (2, blue)) {
  //   block(
  //     for i in range(97, 123) {
  //       text(
  //         features: (ssty: ssty),
  //         [
  //           #stack(dir: ttb)[
  //             #box(eval(str.from-unicode(i), mode: "math"), stroke: 0.01em + black)
  //           ][
  //             #box(text(style: "italic", str.from-unicode(i)), stroke: 0.01em + black)
  //           ]
  //         ],
  //         stroke: 0.01em + color,
  //         fill: black,
  //         top-edge: "bounds",
  //         bottom-edge: "baseline",
  //       )
  //     },
  //   )
  // }
]
