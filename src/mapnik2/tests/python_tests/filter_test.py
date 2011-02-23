#!/usr/bin/env python

from nose.tools import *
from mapnik2.tests.python_tests.utilities import Todo

import mapnik2

if hasattr(mapnik2,'Expression'):
    mapnik2.Filter = mapnik2.Expression

map_ = '''<Map>
    <Style name="s">
        <Rule>
            <Filter><![CDATA[(([region]>=0) and ([region]<=50))]]></Filter>
        </Rule>
        <Rule>
            <Filter><![CDATA[([region]>=0) and ([region]<=50)]]></Filter>
        </Rule>
        <Rule>
            <Filter>
            
            <![CDATA[

            ([region] >= 0) 

            and 

            ([region] <= 50)
            ]]>
            
            </Filter>
        </Rule>
        <Rule>
            <Filter>([region]&gt;=0) and ([region]&lt;=50)</Filter>
        </Rule>
        <Rule>
            <Filter>
            ([region] &gt;= 0)
             and
            ([region] &lt;= 50)
            </Filter>
        </Rule>

    </Style>
    <Style name="s2" filter-mode="first">
        <Rule>
        </Rule>
        <Rule>
        </Rule>
    </Style>
</Map>'''

def test_filter_init():    
    m = mapnik2.Map(1,1)
    mapnik2.load_map_from_string(m,map_)
    filters = []
    filters.append(mapnik2.Filter("([region]>=0) and ([region]<=50)"))
    filters.append(mapnik2.Filter("(([region]>=0) and ([region]<=50))"))
    filters.append(mapnik2.Filter("((([region]>=0) and ([region]<=50)))"))
    filters.append(mapnik2.Filter('((([region]>=0) and ([region]<=50)))'))
    filters.append(mapnik2.Filter('''((([region]>=0) and ([region]<=50)))'''))
    filters.append(mapnik2.Filter('''
    ((([region]>=0)
    and
    ([region]<=50)))
    '''))
    filters.append(mapnik2.Filter('''
    ([region]>=0)
    and
    ([region]<=50)
    '''))
    filters.append(mapnik2.Filter('''
    ([region]
    >=
    0)
    and
    ([region]
    <= 
    50)
    '''))
    
    s = m.find_style('s')
    
    for r in s.rules:
        filters.append(r.filter)
    
    first = filters[0]
    for f in filters:
        eq_(str(first),str(f))
    
    s = m.find_style('s2')
    
    eq_(s.filter_mode,mapnik2.filter_mode.FIRST)
