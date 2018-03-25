#!/usr/bin/env python3
import os
import urllib.parse
import argparse
import sys

import mapnik

API_BASE = 'http://terrain.party/api/export'
MAP_DIMENSIONS = (1081, 1081)
PREFIX = 'addwater_'

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
    line_symbolizer.stroke = mapnik.Color('#000000')
    line_symbolizer.stroke_width = 0.9
    line_symbolizer.stroke_linecap = mapnik.stroke_linecap.ROUND_CAP
    r.symbols.append(line_symbolizer)

    s = mapnik.Style()
    s.rules.append(r)
    return s

def getmap(waterfile, waterwaysfile, boundingbox):
    m = mapnik.Map(*MAP_DIMENSIONS)

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

    extent = mapnik.Box2d(*boundingbox)
    m.aspect_fix_mode = mapnik.aspect_fix_mode.RESPECT
    m.zoom_to_box(extent)

    return m

def coordinates_from_readme(fp):
    for line in fp:
        if API_BASE in line:
            url = line.strip()
            parsed = urllib.parse.urlparse(url)
            qs = urllib.parse.parse_qs(parsed.query)
            box, = qs['box']
            return box

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('partyexport', help='directory where extracted '\
                                            'terarain.party map lives')
    parser.add_argument('waterways', help='path to "waterways" .shp file')
    parser.add_argument('water', help='path to "water" .shp file')
    args = parser.parse_args()

    exportdir = os.listdir(args.partyexport)
    backgrounds = filter(lambda s: s.endswith('png'), exportdir)
    # make sure if the script is run twice we ignore files we've
    # generated
    backgrounds = filter(lambda s: not s.startswith(PREFIX), backgrounds)
    readme, = filter(lambda s: s.endswith('README.txt'), exportdir)

    with open(os.path.join(args.partyexport, readme), 'r') as fp:
        boxstr = coordinates_from_readme(fp)

    box = map(float, boxstr.split(','))
    m = getmap(args.waterways, args.water, box)


    for background in backgrounds:
        m.background_image = os.path.join(args.partyexport, background)
        newfile = ''.join([PREFIX, background])
        mapnik.render_to_file(m, os.path.join(args.partyexport, newfile), 'png')
