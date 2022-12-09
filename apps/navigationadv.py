import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container
from index import app


# bootstrap uses 12 col system
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row([
                dbc.Col([
                    html.Img(src=app.get_asset_url('logo2.png'), height="60px"),
                    dbc.NavbarBrand('Robotic-Assembly Line Dashboard', style={'color': 'black', 'fontSize': 20}, className = 'ms-4')
                ], width = {'size':'auto'})
            ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Nav([
                            dbc.NavItem(dbc.NavLink('Home', href = '/')),
                            # dbc.NavItem(dbc.NavLink('Drill Torque Gauge', href = '/apps/gauge')),
                            dbc.NavItem(dbc.NavLink('Live-Graph', href = '/apps/graph')),
                            # dbc.NavItem(dbc.DropdownMenu(
                            #     children = [
                            #         dbc.DropdownMenuItem('More pages etc.', header = True),
                            #         dbc.DropdownMenuItem('Extra component', href = '/extras')
                            #     ],
                            #         nav = True,
                            #         in_navbar = True,
                            #         label = 'More'
                            #                             ))
                                ],
                                    navbar=True
                                )
                            ], width={'size':'auto'})
                        ], align='center')
            ],
        fluid = True
        )
)
