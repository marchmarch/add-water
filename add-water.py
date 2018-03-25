import mapnik
m = mapnik.Map(1081,1081)
m.background_image='data/test.png'

def water_rule():
    r = mapnik.Rule()
    polygon_symbolizer = mapnik.PolygonSymbolizer()
    polygon_symbolizer.fill = mapnik.Color('#000000')
    r.symbols.append(polygon_symbolizer)

    line_symbolizer = mapnik.LineSymbolizer()
    line_symbolizer.stroke = mapnik.Color('rgb(0%,0%,0%)')
    line_symbolizer.stroke_width = 0.1
    line_symbolizer.stroke_linecap = mapnik.stroke_linecap.ROUND_CAP
    r.symbols.append(line_symbolizer)

    s = mapnik.Style()
    s.rules.append(r)
    return s

def stream_rule():
    r = mapnik.Rule()

    line_symbolizer = mapnik.LineSymbolizer()
    line_symbolizer.stroke = mapnik.Color('rgb(0%,0%,0%)')
    line_symbolizer.stroke_width = 0.9
    line_symbolizer.stroke_linecap = mapnik.stroke_linecap.ROUND_CAP
    r.symbols.append(line_symbolizer)

    s = mapnik.Style()
    s.rules.append(r)
    return s


m.append_style('waterstyle', water_rule())
ds = mapnik.Shapefile(file='data/gis.osm_water_a_free_1.shp')
layer = mapnik.Layer('water')
layer.datasource = ds
layer.styles.append('waterstyle')
m.layers.append(layer)

m.append_style('streamstyle', stream_rule())
ds = mapnik.Shapefile(file='data/gis.osm_waterways_free_1.shp')
layer = mapnik.Layer('stream')
layer.datasource = ds
layer.styles.append('streamstyle')
m.layers.append(layer)


extent = mapnik.Box2d(-72.568043,41.846021,-72.7851035,41.684325)
m.aspect_fix_mode = mapnik.aspect_fix_mode.RESPECT
m.zoom_to_box(extent)
print(m.envelope())
mapnik.render_to_file(m,'world.png', 'png')
print("rendered image to 'world.png'")
