-- A Mandelbrot-implementation written by hand.  The sequential loop
-- is outside the map nest.

default(f32)

type complex = (f32, f32)

fun f32 dot(complex c) =
  let (r, i) = c in
  r * r + i * i

fun complex multComplex(complex x, complex y) =
  let (a, b) = x in
  let (c, d) = y in
  (a*c - b * d,
   a*d + b * c)

fun complex addComplex(complex x, complex y) =
  let (a, b) = x in
  let (c, d) = y in
  (a + c,
   b + d)

fun [screenY][screenX]int mandelbrot(int screenX, int screenY, int depth, (f32,f32,f32,f32) view) =
  let (xmin, ymin, xmax, ymax) = view
  let sizex = xmax - xmin
  let sizey = ymax - ymin
  let c0s = reshape((screenX*screenY),
                    map(fn [screenX]complex (int y) =>
                          map (fn complex (int x) =>
                                 (xmin + (f32(x) * sizex) / f32(screenX),
                                  ymin + (f32(y) * sizey) / f32(screenY)),
                               iota(screenX)),
                        iota(screenY)))
  let escapes = replicate(screenY*screenX, 0)
  loop ((cs, escapes) = (c0s, escapes)) = for i < depth do
    unzip(zipWith(fn (complex, int) (complex c0, complex c, int j) =>
                    (addComplex(c0, multComplex(c, c)),
                     j + if dot(c) < 4.0 then 1 else 0),
                  c0s, cs, escapes))
  in reshape((screenX,screenY), escapes)

fun f32 main() =
  let depth = 255
  let screenX = 1000
  let screenY = 1000
  let view = (-2.0, -0.75, 0.75, 0.75)
  let escapes = mandelbrot(screenX, screenY, depth, view)
  in reduce(+, 0.0, reshape((1000*1000),
                            map(fn [screenX]f32 ([]int row) =>
                                  map(/f32(depth), map(f32, row)),
                                escapes)))
